from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class AuthTestCase(APITestCase):
    def setUp(self):
        self.username = 'usuario_teste'
        self.password = 'senha123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_registro_usuario(self):
        """
        Testa se o registro de um novo usuário está funcionando corretamente.
        """
        data = {
            'username': 'novo_usuario',
            'password': 'nova_senha'
        }
        response = self.client.post('/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Registration successful')

    def test_login_usuario(self):
        """
        Testa se o login com JWT retorna os tokens de acesso e refresh.
        """
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Armazena tokens para uso em outros testes
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_perfil_autenticado(self):
        """
        Testa se o endpoint de perfil só funciona com autenticação.
        """
        # Login para obter o token
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)
        access_token = response.data['access']

        # Envia o token no cabeçalho da requisição
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout_usuario(self):
        """
        Testa se o logout com refresh token funciona e adiciona o token na blacklist.
        """
        # Login
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        # Faz logout com o refresh token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post('/auth/logout/', {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Logout successful')

    def test_tentar_acessar_perfil_apos_logout(self):
        """
        Testa se o endpoint de perfil só funciona com autenticação.
        """
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)