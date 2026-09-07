import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stock_prediction.settings')

application = get_wsgi_application()

# Preload data when server starts (CRITICAL for performance)
print("=" * 60)
print("PRELOADING STOCK DATA...")
print("=" * 60)

try:
    from predictor.views import initialize_global_data
    initialize_global_data()
    print("✓ Stock data preloaded successfully!")
except Exception as e:
    print(f"✗ Error preloading data: {e}")
    print("  App will load data on first request")

print("=" * 60)