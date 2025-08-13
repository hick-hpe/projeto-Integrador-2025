from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class Aluno(AbstractUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
    

class Codigo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    criado_em = models.DateTimeField(auto_now_add=True)

    def expirado(self):
        return self.criado_em < timezone.now() - timedelta(minutes=3)

    def __str__(self):
        return f"Código para {self.user.username}"
    

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Quiz(models.Model):
    NIVEIS = (
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    )
    disciplina = models.ForeignKey(Disciplina, related_name='quizzes', on_delete=models.CASCADE)
    nivel = models.CharField(max_length=13, choices=NIVEIS, default='iniciante')
    descricao = models.TextField()

    def __str__(self):
        return self.descricao[:30] + '...'


class Questao(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questoes', on_delete=models.CASCADE)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.quiz.descricao[:30]}: {self.descricao[:50]}..."


class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.texto}"


class Resposta(models.Model):
    questao = models.OneToOneField(Questao, related_name='resposta', on_delete=models.CASCADE)
    alternativa = models.OneToOneField(Alternativa, on_delete=models.CASCADE)
    explicacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resposta para Questão {self.questao.id} - Alternativa: {self.alternativa.texto}"


class Desempenho(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    num_acertos = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.disciplina} '{self.quiz}': acertou {self.num_acertos} questão(ões)"    
    
    
class RespostaAluno(models.Model):
    desempenho = models.ForeignKey(Desempenho, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, related_name='respostas_explicativas', on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - Questão {self.questao.id} - Alternativa: {self.alternativa.texto} (Tentativa {self.tentativa})" 


class Certificado(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    percentual_acertos = models.IntegerField(default=0)
    data_emissao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.disciplina.nome} - {self.data_emissao}"


class Feedback(models.Model):
    assunto = models.CharField(max_length=20, null=True)
    mensagem = models.TextField(max_length=300, null=True)
    email = models.EmailField(max_length=30, null=True)
    
    def __str__(self):
        return self.assunto or "Feedback sem assunto"


class Emblema(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='emblemas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.aluno.username}"

