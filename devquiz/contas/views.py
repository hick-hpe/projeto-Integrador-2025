from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    View que autentica o usuário e armazena os tokens JWT em cookies HttpOnly.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            # Define cookies seguros para os tokens
            response.set_cookie(
                key='access_token',
                value=access_token,
                max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            # Remove tokens do corpo da resposta (uso apenas via cookie)
            response.data.pop('access', None)
            response.data.pop('refresh', None)

        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    View de registro de usuário.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': 'Username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Username already exists'}, status=400)

    User.objects.create_user(username=username, password=password)
    return Response({'detail': 'Registration successful'}, status=201)


@api_view(['GET'])
def profile_view(request):
    """
    Retorna os dados do perfil do usuário autenticado.
    """
    if not request.user or not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    mensagem = f'Bem vindo, {request.user.username}'
    return Response({'detail': mensagem})


@api_view(['POST'])
def logout_view(request):
    """
    Invalida o refresh token e remove os cookies.
    """
    try:
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response({"detail": "Logout successful"}, status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=400)
