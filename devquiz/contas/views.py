from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, password=password)
    return Response({'detail': 'Registration successful'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    mensagem = f'Bem vindo, {request.user.username}'
    print("Acessando o perfil do usuário:", request.user.username)
    print(mensagem)
    return Response({'message': mensagem})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]             
        token = RefreshToken(refresh_token)                 
        token.blacklist()                                   
        return Response({"detail": "Logout successful"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)