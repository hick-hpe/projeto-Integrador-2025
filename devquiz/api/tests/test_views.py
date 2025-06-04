from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Disciplina, Quiz, Questao, Alternativa, Resposta, Desempenho, Certificado
from rest_framework import status


class QuizTestCase(APITestCase):
    def setUp(self):
        self.username = 'teste'
        self.password = 'senha123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.disciplina = Disciplina.objects.create(nome='Desenvolvimento Web II')
        self.quiz = Quiz.objects.create(disciplina=self.disciplina, nivel='iniciante', descricao='Quiz de Django')
        self.questao = Questao.objects.create(
            quiz=self.quiz, descricao='O que é Django?',
            explicacao='Django é um framework em Python para construir aplicações web.'
        )
        self.alternativa = Alternativa.objects.create(questao=self.questao, texto='Um framework em Python.')
        self.resposta = Resposta.objects.create(questao=self.questao, alternativa=self.alternativa)
        self.desempenho = Desempenho.objects.create(
            user=self.user,
            disciplina=self.disciplina,
            quiz=self.quiz,
            num_acertos=0
        )
        self.certificados = Certificado.objects.create(
            codigo="CERT12345",
            usuario=self.user,
            disciplina=self.disciplina,
        )
        
    def autenticar(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/auth/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica se os cookies foram definidos corretamente
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
    
    def test_listar_disciplinas(self):
        self.autenticar()
        response = self.client.get('/api/disciplinas/')
        self.assertEqual(response.status_code, 200)

    def test_listar_quizzes_disciplina(self):
        self.autenticar()
        response = self.client.get(f'/api/disciplinas/{self.disciplina.id}/quizzes/')
        self.assertEqual(response.status_code, 200)

    def test_listar_questoes_quiz(self):
        self.autenticar()
        response = self.client.get(f'/api/quizzes/{self.quiz.id}/questoes/')
        self.assertEqual(response.status_code, 200)

    def test_detalhe_questao_get(self):
        self.autenticar()
        response = self.client.get(f'/api/quizzes/{self.quiz.id}/questoes/{self.questao.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_iniciar_quiz(self):
        self.autenticar()
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/iniciar/')
        self.assertEqual(response.status_code, 200)

    def test_responder_questao_post(self):
        self.autenticar()
        data = {
            "alternativa_id": self.alternativa.id
        }
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/questoes/{self.questao.id}/', data)
        self.assertEqual(response.status_code, 200)

    def test_certificado_not_found(self):
        self.autenticar()
        response = self.client.get('/api/certificados/codigoinvalido/')
        self.assertEqual(response.status_code, 404)
    
    def test_certificado_certo(self):
        self.autenticar()
        response = self.client.get('/api/certificados/CERT12345/')
        self.assertEqual(response.status_code, 200)

    def test_desistir_quiz(self):
        self.autenticar()
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/desistir/')
        self.assertEqual(response.status_code, 200)

    def test_concluir_quiz(self):
        self.autenticar()
        Desempenho.objects.create(user=self.user, disciplina=self.disciplina, quiz=self.quiz, num_acertos=1)
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/concluir/')
        self.assertEqual(response.status_code, 200)