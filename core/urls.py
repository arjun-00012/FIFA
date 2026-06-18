from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django base system management access route portal
    path('admin/', admin.site.urls),
    
    # Injects the complete app endpoints block to mount at baseline root level
    path('', include('auction.urls')),
]

# CRITICAL FOR FILE PICKERS: Tells Django how to find and render images uploaded from your system
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)