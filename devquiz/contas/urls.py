from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('teste-autenticacao/', UserDetailView.as_view(), name='teste_autenticacao'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('enviar-email/', EnviarEmailView.as_view(), name='enviar_mail'),
    path('validar-codigo/', ValidarCodigoView.as_view(), name='validar_codigo'),
    path('conta-detail/', ContaDetailView.as_view(), name='conta'),

    # JWT com cookies
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
    