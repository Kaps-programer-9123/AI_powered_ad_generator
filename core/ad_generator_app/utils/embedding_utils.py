# ad_generator_app/utils/embedding_utils.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
EMBEDDING_MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
EMBEDDING_DIM = EMBEDDING_MODEL.get_sentence_embedding_dimension()

def load_and_embed_data(file_path, text_key):
    with open(file_path, 'r') as f:
        data = json.load(f)
    texts = [item[text_key] for item in data]
    embeddings = EMBEDDING_MODEL.encode(texts)
    return data, embeddings

def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    return index

def search_faiss_index(index, query, top_k=3):
    query_embedding = EMBEDDING_MODEL.encode([query]).astype('float32')
    D, I = index.search(query_embedding, top_k)
    return D[0], I[0]

def get_relevant_data(data, indices):
    return [data[i] for i in indices]

if __name__ == '__main__':
    # Example usage:
    product_data, product_embeddings = load_and_embed_data('../../../data/products.json', 'description')
    product_index = build_faiss_index(product_embeddings)

    blog_data, blog_embeddings = load_and_embed_data('../../../data/blog_posts.json', 'content')
    blog_index = build_faiss_index(blog_embeddings)

    query = "comfortable shoes for walking"
    product_distances, product_indices = search_faiss_index(product_index, query)
    relevant_products = get_relevant_data(product_data, product_indices)
    print("Relevant Products:", relevant_products)

    blog_distances, blog_indices = search_faiss_index(blog_index, query)
    relevant_blogs = get_relevant_data(blog_data, blog_indices)
    print("Relevant Blogs:", relevant_blogs)