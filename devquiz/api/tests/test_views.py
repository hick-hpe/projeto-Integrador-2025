from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Disciplina, Quiz, Questao, Alternativa, Resposta, Desempenho, Certificado


class QuizTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha123')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.disciplina = Disciplina.objects.create(nome='Desenvolvimento Web II')
        self.quiz = Quiz.objects.create(disciplina=self.disciplina, nivel='iniciante', descricao='Quiz de Django')
        self.questao = Questao.objects.create(quiz=self.quiz, descricao='O que é Django?', explicacao='Django é um framework em Python para construir aplicações web.')
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
    
    def test_listar_disciplinas(self):
        response = self.client.get('/api/disciplinas/')
        self.assertEqual(response.status_code, 200)

    def test_listar_quizzes_disciplina(self):
        response = self.client.get(f'/api/disciplinas/{self.disciplina.id}/quizzes/')
        self.assertEqual(response.status_code, 200)

    def test_listar_questoes_quiz(self):
        response = self.client.get(f'/api/quizzes/{self.quiz.id}/questoes/')
        self.assertEqual(response.status_code, 200)

    def test_detalhe_questao_get(self):
        response = self.client.get(f'/api/quizzes/{self.quiz.id}/questoes/{self.questao.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_iniciar_quiz(self):
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/iniciar/')
        self.assertEqual(response.status_code, 200)

    def test_responder_questao_post(self):
        data = {
            "alternativa_id": self.alternativa.id
        }
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/questoes/{self.questao.id}/', data)
        self.assertEqual(response.status_code, 200)

    def test_certificado_not_found(self):
        response = self.client.get('/api/certificados/codigoinvalido/')
        self.assertEqual(response.status_code, 404)
    
    def test_certificado_certo(self):
        response = self.client.get('/api/certificados/CERT12345/')
        self.assertEqual(response.status_code, 200)

    def test_desistir_quiz(self):
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/desistir/')
        self.assertEqual(response.status_code, 200)

    def test_concluir_quiz(self):
        Desempenho.objects.create(user=self.user, disciplina=self.disciplina, quiz=self.quiz, num_acertos=1)
        response = self.client.post(f'/api/quizzes/{self.quiz.id}/concluir/')
        self.assertEqual(response.status_code, 200)