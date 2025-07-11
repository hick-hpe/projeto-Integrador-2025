from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from api.models import Codigo
from api.serializers import UserSerializer

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
                samesite='Strict'
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                httponly=True,
                secure=False,
                samesite='Strict'
            )

            # produção:
            # secure=True, samesite='None'

            # Remove tokens do corpo da resposta (uso apenas via cookie)
            response.data.pop('access', None)
            response.data.pop('refresh', None)
            response.data['detail'] = 'Login realizado com sucesso!!'

        return response


class CadastroView(APIView):
    """
    View de registro de usuário.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm-password')

        if all([username, email, password, confirm_password]):
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Este usuário já existe!'}, status=status.HTTP_400_BAD_REQUEST)

            if password != confirm_password:
                return Response({'error': 'As senhas não coindizem!'}, status=status.HTTP_400_BAD_REQUEST)

            User.objects.create_user(username=username, password=password)
            return Response({'detail': 'Conta criada com sucesso!!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Preencha os campos!'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    View para obter detalhes do usuário autenticado.
    """
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Invalida o refresh token e remove os cookies.
    """

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def gerar_codigo_recuperacao():
    """
    Gera um código de recuperação aleatório.
    """
    return str(randint(100000, 999999))


class EnviarEmailView(APIView):
    """
    View para enviar um código de recuperação por e-mail.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email é obrigatório!'}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            return Response({'detail': 'Email não cadastrado!'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Erro inesperado ao buscar o usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        codigo_gerado = gerar_codigo_recuperacao()
        assunto = "Código enviado!"
        mensagem = f"Seu código de recuperação é: {codigo_gerado}"

        try:
            send_mail(assunto, mensagem, settings.EMAIL_HOST_USER, [email])
            Codigo.objects.create(user=user, codigo=codigo_gerado)
            return Response({'detail': 'Código enviado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'Erro ao enviar o e-mail: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidarCodigoView(APIView):
    """
    View para validar o código recebido por e-mail.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        codigo_recebido = request.data.get('codigo')

        if not email or not codigo_recebido:
            return Response({'detail': 'Email e código são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(email=email).exists():
            return Response({'detail': 'Email não cadastrado'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            codigo_obj = Codigo.objects.filter(user=user, codigo=codigo_recebido).first()

            if not codigo_obj:
                return Response({'detail': 'Código inválido'}, status=status.HTTP_400_BAD_REQUEST)

            if codigo_obj.expirado():
                return Response({'detail': 'Código expirado'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Código válido'})


class ContaDetailView(APIView):
    """
    View para atualizar ou excluir a conta do usuário autenticado.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Dados atualizados'})
    
    def delete(self, request):
        request.user.delete()
        return Response({'detail': 'Conta excluída com sucesso'})
