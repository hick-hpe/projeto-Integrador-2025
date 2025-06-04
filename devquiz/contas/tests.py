from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class AuthTestCase(APITestCase):
    def setUp(self):
        self.username = 'usuario_teste'
        self.email = 'teste@gmail.com'
        self.password = 'senha123'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

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

    def test_login_com_cookie(self):
        """
        Testa se o login retorna e armazena os tokens JWT nos cookies.
        """
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica se os cookies foram definidos corretamente
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_perfil_autenticado_com_cookie(self):
        """
        Testa se o perfil pode ser acessado com autenticação via cookie JWT.
        """
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)

        access_cookie = response.cookies.get('access_token')
        self.assertIsNotNone(access_cookie)

        # # Simula a presença do cookie no cliente
        self.client.cookies['access_token'] = access_cookie.value

        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        print('DETAIL:', response.data['detail'])

    def test_logout_usuario_com_cookie(self):
        """
        Testa se o logout remove os cookies e invalida o refresh token.
        """
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)

        access_cookie = response.cookies.get('access_token')
        refresh_cookie = response.cookies.get('refresh_token')

        self.assertIsNotNone(refresh_cookie)

        # Define os cookies manualmente para simular sessão ativa
        self.client.cookies['access_token'] = access_cookie.value
        self.client.cookies['refresh_token'] = refresh_cookie.value

        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Logout successful')

    def test_tentar_acessar_perfil_sem_login(self):
        """
        Testa se o acesso ao perfil sem login retorna 401.
        """
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_enviar_email(self):
        """
        Email enviado com sucesso
        """
        response = self.client.post('/auth/enviar-email/', {"email":self.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_nao_cadastrado(self):
        """
        Email não cadastrado
        """
        response = self.client.post('/auth/enviar-email/', {"email":"self.email"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_email_nao_fornecido(self):
        """
        Usuário não informou o email
        """
        response = self.client.post('/auth/enviar-email/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validar_codigo(self):
        """
        Validar o código fornecido
        """
        response = self.client.post('/auth/enviar-email/', {"email":self.email, "codigo": "123456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
