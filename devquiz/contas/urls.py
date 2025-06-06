# contas/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('teste-autenticacao/', views.usuario_autenticado, name='teste_autenticacao'),
    path('logout/', views.logout, name='logout'),
    path('enviar-email/', views.enviar_mail, name='enviar_mail'),
    path('valida-codigo/', views.validar_codigo, name='validar_codigo'),

    # JWT com cookies
    path('token/', views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
