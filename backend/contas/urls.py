from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # cadastro
    path('cadastro/', CadastroView.as_view(), name='cadastro'),

    # dados do usuario logado
    path("me/", UserDetailView.as_view(), name="auth_me"),

    # logout
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # recuperacao de conta
    # path('enviar-email/', EnviarEmailView.as_view(), name='enviar_mail'),
    # path('validar-codigo/', ValidarCodigoView.as_view(), name='validar_codigo'),

    # atualizar/deletar conta
    path('conta/', ContaDetailView.as_view(), name='conta'),

    # JWT com cookies -> login e refresh token
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
    