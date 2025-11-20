from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class CustomUser(models.Model):
    TIPOS_USUARIOS_CHOICE = [
        ('aluno', 'aluno'),
        ('admin', 'admin'),
    ]
    user = models.OneToOneField(User, related_name='aluno', on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    matricula = models.CharField(max_length=16, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=5, choices=TIPOS_USUARIOS_CHOICE)

    def __str__(self):
        return f"{self.user}"
    

class Codigo(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
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
    nivel = models.CharField(max_length=13, choices=NIVEIS, default='Iniciante')
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
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    num_acertos = models.IntegerField(default=0)
    concluiu_quiz = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.disciplina} '{self.quiz}': acertou {self.num_acertos} questão(ões)"    


class Tentativa(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    desempenho = models.ForeignKey(Desempenho, on_delete=models.CASCADE, null=True, blank=True)
    concluiu_quiz = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.aluno} - Tentativa {self.pk} - Concluída: {self.concluiu_quiz}'
    

class RespostaAluno(models.Model):
    desempenho = models.ForeignKey(Desempenho, on_delete=models.CASCADE, null=True, blank=True)
    questao = models.ForeignKey(Questao, related_name='respostas_explicativas', on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.desempenho.aluno.user.username} - Questão {self.questao.pk} - Alternativa: {self.alternativa.texto}" 


class Certificado(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    percentual_acertos = models.IntegerField(default=0)
    data_emissao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno} - {self.disciplina.nome} - {self.data_emissao}"


class Feedback(models.Model):
    assunto = models.CharField(max_length=20, null=True, default="Feedback sem assunto")
    mensagem = models.TextField(max_length=300, null=True)
    email = models.EmailField(max_length=30, null=True)
    
    def __str__(self):
        return self.assunto


class Emblema(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    logo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}: {self.descricao}"
    

class EmblemaUser(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    emblema = models.ForeignKey(Emblema, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.nome} - {self.emblema}"


class Pontuacao(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pontos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.aluno} - {self.pontos} pontos'


