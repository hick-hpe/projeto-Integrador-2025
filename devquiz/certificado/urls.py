from django.urls import path
from . import views

urlpatterns = [
    # Certificado
    path('<str:codigo>/', views.certificados, name='certificado'),
    path('<str:codigo>/download/', views.certificados_download, name='certificado'),
]