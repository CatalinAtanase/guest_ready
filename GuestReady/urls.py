from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from reservations.views import load_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservation/', include('reservations.urls', namespace='reservations')),
    path('api-auth/', include('rest_framework.urls')),
    path('', load_csv, name="load_csv"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
