from django.apps import AppConfig


class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'
    
    def ready(self):
        '''Initialize data when Django starts'''
        print("[STARTUP] Initializing stock data cache...")
        try:
            from .views import initialize_global_data
            initialize_global_data()
            print("[STARTUP] ✓ Stock data cache ready!")
        except Exception as e:
            print(f"[STARTUP] ✗ Error: {e}")