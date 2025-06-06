from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('contas.urls')),
    path('certificados/', include('certificado.urls')),
    path('', views.index)
]
