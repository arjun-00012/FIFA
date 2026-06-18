from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  
from django.urls import re_path

urlpatterns = [
    # Django base system management access route portal
    path('admin/', admin.site.urls),
    
    # Injects the complete app endpoints block to mount at baseline root level
    path('', include('auction.urls')),
]

# CRITICAL FOR FILE PICKERS: Tells Django how to find and render images uploaded from your system
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    # Local development server route
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)