# ad_generator_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
# Import your AppConfig
from ad_generator_app.apps import AdGeneratorAppConfig
import logging

log = logging.getLogger(__name__)

# Access the pre-initialized RAGPipeline instance
# This will be None until the app is ready, but by the time views are called, it will be set.
rag_pipeline = AdGeneratorAppConfig.rag_pipeline_instance

def generate_ad(request):
    # Ensure the pipeline is ready before using it
    if rag_pipeline is None:
        log.error("RAGPipeline is not initialized. Check app startup.")
        return JsonResponse({'error': 'AI services are not ready. Please try again later.'}, status=503)

    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            try:
                results = rag_pipeline.run(query)
                return JsonResponse({
                    'query': results['query'],
                    'ad_copy': results['ad_copy'],
                    'relevant_products': results['relevant_products'],
                    'relevant_blogs': results['relevant_blogs']
                })
            except Exception as e:
                log.error(f"Error processing query '{query}': {e}")
                return JsonResponse({'error': f'An error occurred during ad generation: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'Please provide a query parameter "q".'})
    else:
        return JsonResponse({'error': 'Only GET requests are supported.'}, status=405)

def home(request):
    return render(request, 'home.html') # Assuming you have this template