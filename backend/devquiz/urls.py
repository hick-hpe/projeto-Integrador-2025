from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('contas.urls')),
    path('api/certificados/', include('certificado.urls')),
    path('api/', include('api.urls')),
]
