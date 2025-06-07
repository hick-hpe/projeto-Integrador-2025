from django.urls import path
from . import views

urlpatterns = [
    # Certificado
    path('gerar/', views.gerar_certificado, name='certificado'), # pelo menos 70%
    path('<str:codigo>/', views.certificados, name='certificado'),
    # path('<str:codigo>/download/', views.certificado_download, name='certificados_download'),
    path('', views.certificado, name='certificado'),
]