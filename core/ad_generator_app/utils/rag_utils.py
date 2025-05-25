# ad_generator_app/utils/rag_utils.py
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate
from sentence_transformers import CrossEncoder
from .embedding_utils import (
    load_and_embed_data,
    build_faiss_index,
    search_faiss_index,
    get_relevant_data,
    EMBEDDING_MODEL
)
import os
from os import getenv
import logging

logging.basicConfig(level=logging.INFO)  # Or DEBUG, WARNING, etc.
log = logging.getLogger(__name__)

# Initialize Cross-Encoder for reranking
RERANKER_MODEL_NAME = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
RERANKER = CrossEncoder(RERANKER_MODEL_NAME)

# You'll need an OpenAI API key if you use OpenAI's models
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
def get_llm():
    key = getenv("OPENROUTER_BASE_URL")
    print("###### "+key)
    llm = ChatOpenAI(
        openai_api_base=getenv("OPENROUTER_BASE_URL"),
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        model_name="google/gemma-3-27b-it:free"
    )
    return llm


def rerank_results(query, documents):
    if not documents:
        return []
    pairs = [[query, doc] for doc in documents]
    scores = RERANKER.predict(pairs)
    ranked_docs = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked_docs]

def generate_ad_copy(query, relevant_products, relevant_blogs=None, llm=None):
    if llm is None:
        return "LLM not configured."

    product_info = "\n".join([f"- {p['name']}: {p['description']}" for p in relevant_products])
    blog_info = ""
    if relevant_blogs:
        blog_info = "\n".join([f"- '{b['title']}': {b['content'][:100]}..." for b in relevant_blogs])

    template = PromptTemplate.from_template(
        """You are an AI advertising agent. Generate a short and compelling ad based on the user's query: '{query}'.
        Incorporate information from the following products:
        {product_info}
        {blog_info}
        Focus on relevance and user interest. Include a call to action if appropriate."""
    )
    log.info("template : %s",template)
    log.info("query : %s",query)
    log.info("product_info:  %s",product_info)
    log.info("blog_info  %s: ",blog_info)
    prompt = template.format(query=query, product_info=product_info, blog_info=blog_info)
    return llm.invoke([HumanMessage(content=prompt)])

class RAGPipeline:
    def __init__(self, product_data_path, blog_data_path):
        self.product_data, product_embeddings = load_and_embed_data(product_data_path, 'description')
        self.product_index = build_faiss_index(product_embeddings)
        self.blog_data, blog_embeddings = load_and_embed_data(blog_data_path, 'content')
        self.blog_index = build_faiss_index(blog_embeddings)
        # Initialize an LLM here if you want to use Langchain's LLM integration
        # self.llm = OpenAI() if os.environ.get("OPENAI_API_KEY") else None
        self.llm = get_llm() # For now, you'd need to replace this with an actual LLM instance

    def run(self, query):
        # 1. Retrieve relevant products
        product_distances, product_indices = search_faiss_index(self.product_index, query, top_k=5)
        relevant_products = get_relevant_data(self.product_data, product_indices)

        # 2. Retrieve relevant blog posts
        blog_distances, blog_indices = search_faiss_index(self.blog_index, query, top_k=3)
        relevant_blogs = get_relevant_data(self.blog_data, blog_indices)

        # 3. Rerank the retrieved content (optional but good for quality)
        product_descriptions = [p['description'] for p in relevant_products]
        reranked_products = rerank_results(query, product_descriptions)
        # Get the original product data based on the reranked descriptions (simplification)
        reranked_relevant_products = [p for p in self.product_data if p['description'] in reranked_products]

        blog_contents = [b['content'] for b in relevant_blogs]
        reranked_blogs = rerank_results(query, blog_contents)
        # Get the original blog data
        reranked_relevant_blogs = [b for b in self.blog_data if b['content'] in reranked_blogs]

        # 4. Generate ad copy using the LLM and retrieved context
        if self.llm:
            log.info("#############################################################")
            log.info("reranked_relevant_products : %s",reranked_relevant_products)
            log.info("reranked_relevant_blogs : %s",reranked_relevant_blogs)
            log.info("query:  %s",query)
            ad_copy_message = generate_ad_copy(query, reranked_relevant_products, reranked_relevant_blogs, self.llm)

            # Safely extract string content
            ad_copy = ad_copy_message.content if hasattr(ad_copy_message, "content") else str(ad_copy_message)

            log.info("Generated ad copy: %s", ad_copy)
        else:
            ad_copy = "Please configure an LLM to generate ad copy."

        return {
            "query": query,
            "relevant_products": reranked_relevant_products,
            "relevant_blogs": reranked_relevant_blogs,
            "ad_copy": ad_copy
        }

# Example usage (outside Django view):
if __name__ == '__main__':
    pipeline = RAGPipeline('../../../data/products.json', '../../../data/blog_posts.json')
    results = pipeline.run("best waterproof hiking boots")
    print(results['ad_copy'])
    print("\nRelevant Products:", results['relevant_products'])
    print("\nRelevant Blogs:", results['relevant_blogs'])