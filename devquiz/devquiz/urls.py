from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('contas.urls')),
    path('api/certificados/', include('certificado.urls')),
    path('api/', include('api.urls')),
]
