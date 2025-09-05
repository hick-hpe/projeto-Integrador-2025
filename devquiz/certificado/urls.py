from django.urls import path
from .views import *

urlpatterns = [
    # Certificado
    path('<str:codigo>/', CertificadoDetailView.as_view(), name='certificado'),
    path('<str:codigo>/download/', CertificadoDownloadView.as_view(), name='certificados_download'),
    path('', CertificadoPDFView.as_view(), name='certificado_list'),
]