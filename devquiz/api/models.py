from django.db import models
from django.contrib.auth.models import User


class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Quiz(models.Model):
    NIVEIS = (
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    )
    disciplina = models.ForeignKey(Disciplina, related_name='quizzes', on_delete=models.CASCADE)
    nivel = models.CharField(max_length=13, choices=NIVEIS, default='iniciante')
    descricao = models.TextField()

    def __str__(self):
        return self.descricao[:50] + '...'


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


class Questao(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questoes', on_delete=models.CASCADE)
    descricao = models.TextField()
    explicacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quiz.descricao[:30]}: {self.descricao[:50]}..."


class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.texto}"


class Resposta(models.Model):
    questao = models.ForeignKey(Questao, related_name='respostas', on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    explicacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resposta para Questão {self.questao.id} - Alternativa: {self.alternativa.texto}"


class RespostaAluno(models.Model):
    aluno = models.ForeignKey(User, related_name='rescpostas_aluno', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, related_name='respostas_explicativas', on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.aluno.user.username} - Questão {self.questao.id} - Alternativa: {self.alternativa.texto}"
    

# class Pontuacao(models.Model):
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     pontuacao = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.usuario.username} - {self.pontuacao} pontos"


class Certificado(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data_emissao = models.DateField(auto_now_add=True)
    # adicionar qr_code

    def __str__(self):
        return f"{self.usuario.username} - {self.disciplina.nome} - {self.data_emissao}"

