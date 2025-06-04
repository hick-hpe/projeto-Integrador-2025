from api.models import *
from django.contrib.auth.models import User

# Busca ou cria a disciplina
disciplina, _ = Disciplina.objects.get_or_create(nome='Desenvolvimento Web II')

# Criação do quiz
quiz = Quiz.objects.create(
    disciplina=disciplina,
    nivel='iniciante',
    descricao='Quiz sobre conceitos básicos de Django.'
)

# Lista de questões e alternativas (com marcação de correta)
questoes = [
    {
        'descricao': 'Django é um framework web escrito em Python.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False}
        ]
    },
    {
        'descricao': 'O comando para criar um novo projeto Django é: django-admin startproject nome_do_projeto.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False}
        ]
    },
    {
        'descricao': 'Qual destes arquivos é responsável pelas rotas (URLs) em um projeto Django?',
        'alternativas': [
            {'texto': 'models.py', 'correta': False},
            {'texto': 'views.py', 'correta': False},
            {'texto': 'urls.py', 'correta': True},
            {'texto': 'admin.py', 'correta': False}
        ]
    },
    {
        'descricao': 'O Django ORM permite manipular o banco de dados usando objetos Python.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False}
        ]
    },
    {
        'descricao': 'Para criar uma nova aplicação em um projeto Django, usamos o comando: python manage.py startapp nome_app.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False}
        ]
    },
    {
        'descricao': 'Qual destes comandos aplica as migrações pendentes no banco de dados?',
        'alternativas': [
            {'texto': 'python manage.py makemigrations', 'correta': False},
            {'texto': 'python manage.py migrate', 'correta': True},
            {'texto': 'python manage.py runserver', 'correta': False},
            {'texto': 'python manage.py createsuperuser', 'correta': False}
        ]
    },
    {
        'descricao': 'O arquivo settings.py armazena as configurações do projeto Django.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False}
        ]
    },
    {
        'descricao': 'Qual destes métodos é usado para consultar todos os objetos de um modelo no Django ORM?',
        'alternativas': [
            {'texto': 'Model.objects.all()', 'correta': True},
            {'texto': 'Model.all()', 'correta': False},
            {'texto': 'Model.get()', 'correta': False},
            {'texto': 'Model.filter()', 'correta': False}
        ]
    },
    {
        'descricao': 'O Django possui um painel administrativo pronto para uso.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False}
        ]
    },
    {
        'descricao': 'Qual comando inicia o servidor de desenvolvimento do Django?',
        'alternativas': [
            {'texto': 'python manage.py runserver', 'correta': True},
            {'texto': 'python manage.py startproject', 'correta': False},
            {'texto': 'python manage.py migrate', 'correta': False},
            {'texto': 'python manage.py shell', 'correta': False}
        ]
    }
]

# Popular o banco com as questões, alternativas e respostas corretas
for q in questoes:
    questao = Questao.objects.create(quiz=quiz, descricao=q['descricao'])

    for alt in q['alternativas']:
        alternativa = Alternativa.objects.create(
            questao=questao,
            texto=alt['texto']
        )
        if alt['correta']:
            Resposta.objects.create(
                questao=questao,
                alternativa=alternativa,
                explicacao="Resposta correta."
            )


certificado, _ = Certificado.objects.create(
    codigo="CERT12345",
    usuario=User.objects.get(pk=1),
    disciplina=disciplina
)