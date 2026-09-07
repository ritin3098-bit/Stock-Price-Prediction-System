from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # include the predictor app WITH a namespace so named reverses like
    # 'predictor:index' work consistently:
    path('', include(('predictor.urls', 'predictor'), namespace='predictor')),
    # provide built-in auth views at /accounts/ (this registers 'login', 'logout', etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

# static/media serving in DEBUG
if settings.DEBUG and settings.STATIC_URL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG and settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
