from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

# ====================================================
# CustomUser - para os usuários 'aluno' e 'admin'
# ====================================================
class CustomUser(models.Model):
    TIPOS_USUARIOS_CHOICE = [
        ('aluno', 'aluno'),
        ('admin', 'admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    matricula = models.CharField(max_length=16)
    tipo_usuario = models.CharField(max_length=5, choices=TIPOS_USUARIOS_CHOICE)

    def __str__(self):
        return f"{self.user}"
    
# ====================================================
# Código de expiração - Recuperar conta
# ====================================================
class Codigo(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6)
    criado_em = models.DateTimeField(auto_now_add=True)

    def expirado(self):
        return self.criado_em < timezone.now() - timedelta(minutes=3)

    def __str__(self):
        return f"Código para {self.aluno.user.username}"
    
# ====================================================
# Disciplina
# ====================================================
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# ====================================================
# Quiz
# ====================================================
class Quiz(models.Model):
    NIVEIS_CHOICE = (
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    )
    TIPOS_QUESTOES_CHOICE = (
        ('Múltipla Escolha', 'Múltipla Escolha'),
        ('Verdadeiro ou Falso', 'Verdadeiro ou Falso'),
        ('Múltipla Escolha e Verdadeiro ou Falso', 'Múltipla Escolha e Verdadeiro ou Falso'),
    )
    titulo = models.CharField(max_length=100, null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, related_name='quizzes', on_delete=models.CASCADE)
    nivel = models.CharField(max_length=13, choices=NIVEIS_CHOICE, default='Iniciante')
    descricao = models.TextField()
    tipo_questoes = models.CharField(max_length=38, choices=TIPOS_QUESTOES_CHOICE, default='Múltipla Escolha')

    def __str__(self):
        return self.descricao[:30] + '...'

# ====================================================
# Questão
# ====================================================
class Questao(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questoes', on_delete=models.CASCADE)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.quiz.descricao[:30]}: {self.descricao[:50]}..."

# ====================================================
# Alternativa
# ====================================================
class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.texto}"

# ====================================================
# Tentativas
# ====================================================
class Tentativa(models.Model):
    STATUS_QUIZ_CHOICE = [
        ('Iniciado', 'Iniciado'),
        ('Desistido', 'Desistido'),
        ('Concluído', 'Concluído'),
    ]
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    status_quiz = models.CharField(max_length=9, choices=STATUS_QUIZ_CHOICE, default='Iniciado')
    aprovado = models.BooleanField(default=False) # atingiu 70%
    pontuacao = models.IntegerField(default=0)
    num_tentativa = models.IntegerField()

    def __str__(self):
        return f'{self.aluno} - Tentativa {self.pk} - Concluída: {self.status_quiz == "Concluído"}'

# ====================================================
# Resposta da questão
# ====================================================
class RespostaQuestao(models.Model):
    questao = models.OneToOneField(Questao, related_name='resposta', on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    explicacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resposta para Questão {self.questao.id} - Alternativa: {self.alternativa.texto}"
    
# ====================================================
# Respostas do aluno
# ====================================================
class RespostaAluno(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, related_name='respostas_explicativas', on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    tentativa = models.ForeignKey(Tentativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tentativa.aluno.user.username} - Questão {self.questao.pk} - Alternativa: {self.alternativa.texto}" 

# ====================================================
# Certificados
# ====================================================
class Certificado(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    percentual_acertos = models.IntegerField(default=0)
    data_emissao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno} - {self.disciplina.nome} - {self.data_emissao}"

# ====================================================
# Emblemas
# ====================================================
class Emblema(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.TextField(max_length=100)
    logo = models.ImageField(upload_to='emblemas/', null=True)

    def __str__(self):
        return f'Emblema {self.nome}'

# ====================================================
# Emblemas do aluno
# ====================================================
class EmblemaUser(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    emblema = models.ForeignKey(Emblema, on_delete=models.CASCADE)
    conquistado_em = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.aluno.user.username} conquistou o emblema {self.emblema.nome}'

# =========================================================================================================================
# Adicionais Futuros
# =========================================================================================================================

# class Feedback(models.Model):
#     assunto = models.CharField(max_length=20, null=True, default="Feedback sem assunto")
#     mensagem = models.TextField(max_length=300, null=True)
#     email = models.EmailField(max_length=30, null=True)
    
#     def __str__(self):
#         return self.assunto


# class Emblema(models.Model):
#     nome = models.CharField(max_length=50)
#     descricao = models.TextField()
#     logo = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return f"{self.nome}: {self.descricao}"
    

# class EmblemaUser(models.Model):
#     aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     emblema = models.ForeignKey(Emblema, on_delete=models.CASCADE, null=True)
    
#     def __str__(self):
#         return f"{self.nome} - {self.emblema}"


# class Pontuacao(models.Model):
#     aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     pontos = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f'{self.aluno} - {self.pontos} pontos'


