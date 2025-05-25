# ad_generator_app/apps.py
from django.apps import AppConfig
import os
import logging

log = logging.getLogger(__name__)

class AdGeneratorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ad_generator_app'
    
    # This will hold our RAGPipeline instance
    rag_pipeline_instance = None

    def ready(self):
        """
        This method is called once when Django starts up.
        We initialize the RAGPipeline here.
        """
        if os.environ.get('RUN_MAIN', None) != 'true':
            # This check prevents running the initialization code twice
            # in environments like Django's runserver which spawns a reloader process.
            # In production (e.g., Gunicorn/uWSGI), RUN_MAIN is typically 'true' for the main process.
            return

        from .utils.rag_utils import RAGPipeline
        
        # Define paths for data files
        # Adjust BASE_DIR calculation for the project root
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_DIR = os.path.join(BASE_DIR, 'data')
        
        PRODUCT_DATA_PATH = os.path.join(DATA_DIR, 'products.json')
        BLOG_DATA_PATH = os.path.join(DATA_DIR, 'blog_posts.json')

        log.info(f"Initializing RAGPipeline...")
        log.info(f"Product data path: {PRODUCT_DATA_PATH}")
        log.info(f"Blog data path: {BLOG_DATA_PATH}")

        # Initialize the pipeline and store it
        try:
            AdGeneratorAppConfig.rag_pipeline_instance = RAGPipeline(PRODUCT_DATA_PATH, BLOG_DATA_PATH)
            log.info("RAGPipeline initialized successfully.")
        except Exception as e:
            log.error(f"Failed to initialize RAGPipeline: {e}")
            # Depending on severity, you might want to raise an exception or handle gracefully
            # For a production app, robust error handling here is crucial.