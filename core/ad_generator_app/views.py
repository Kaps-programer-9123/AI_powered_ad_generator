# ad_generator_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils.rag_utils import RAGPipeline
import os
import logging 

log = logging.getLogger(__name__)
# Initialize the RAG pipeline (ideally, do this once at app startup)
PRODUCT_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'products.json')
BLOG_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'blog_posts.json')
log.info("product data path : "+str(PRODUCT_DATA_PATH))
log.info("blog data path : "+str(BLOG_DATA_PATH))
rag_pipeline = RAGPipeline(PRODUCT_DATA_PATH, BLOG_DATA_PATH)

def generate_ad(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            results = rag_pipeline.run(query)
            return JsonResponse({
                'query': results['query'],
                'ad_copy': results['ad_copy'],
                'relevant_products': results['relevant_products'],
                'relevant_blogs': results['relevant_blogs']
            })
        else:
            return JsonResponse({'error': 'Please provide a query parameter "q".'})
    else:
        return JsonResponse({'error': 'Only GET requests are supported.'}, status=405)

def home(request):
    return render(request, 'home.html')