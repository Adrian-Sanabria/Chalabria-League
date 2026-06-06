from django.contrib import admin
from django.urls import path
from futbol.views import inicio

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)