
# # Criar disciplina
# from api.models import *


# disciplina = Disciplina.objects.create(nome='Desenvolvimento Web II')

# # Criar quiz
# quiz = Quiz.objects.create(
#     disciplina=disciplina,
#     nivel='iniciante',
#     descricao='Teste seus conhecimentos em Desenvolvimento Web II\nBásico de Django e Python'
# )

# # Criar questão
# questao = Questao.objects.create(
#     quiz=quiz,
#     descricao='O que é Django?',
#     resposta_correta=1
# )

# # Criar 4 alternativas
# a1 = Alternativa.objects.create(questao=questao, texto='Um framework web para Python', correta=True)
# a2 = Alternativa.objects.create(questao=questao, texto='Uma biblioteca de JavaScript', correta=False)
# a3 = Alternativa.objects.create(questao=questao, texto='Um banco de dados', correta=False)
# a4 = Alternativa.objects.create(questao=questao, texto='Um sistema operacional', correta=False)

# # Criar resposta
# Resposta.objects.create(
#     questao=questao,
#     alternativa=a1
# )

# # Criar resposta explicativa
# RespostaExplicacao.objects.create(
#     questao=questao,
#     texto='Django é um framework web de alto nível que estimula o desenvolvimento rápido e limpo de aplicações web.'
# )

# # Criar questao 2
# questao2 = Questao.objects.create(
#     quiz=quiz,
#     descricao='Qual é a linguagem de programação usada pelo Django?',
# )
# # Criar 4 alternativas para a questão 2
# a1 = Alternativa.objects.create(questao=questao2, texto='Java', correta=False)
# a2 = Alternativa.objects.create(questao=questao2, texto='JavaScript', correta=False)
# a3 = Alternativa.objects.create(questao=questao2, texto='Python', correta=True)
# a4 = Alternativa.objects.create(questao=questao2, texto='C#', correta=False)

# # Criar resposta para a questão 2
# Resposta.objects.create(
#     questao=questao2,
#     alternativa=a3
# )

# # Criar resposta explicativa para a questão 2
# RespostaExplicacao.objects.create(
#     questao=questao2,
#     texto='Django é um framework web que utiliza a linguagem de programação Python.'
# )

# # Criar questao 3
# questao3 = Questao.objects.create(
#     quiz=quiz,
#     descricao='Qual é o comando para iniciar um projeto Django?',
# )

# # Criar 4 alternativas para a questão 3
# a1 = Alternativa.objects.create(questao=questao3, texto='django startproject', correta=False)
# a2 = Alternativa.objects.create(questao=questao3, texto='django-admin startproject', correta=True)
# a3 = Alternativa.objects.create(questao=questao3, texto='startproject django', correta=False)
# a4 = Alternativa.objects.create(questao=questao3, texto='django-admin createproject', correta=False)

# # Criar resposta para a questão 3
# Resposta.objects.create(
#     questao=questao3,
#     alternativa=a2
# )

# # Criar resposta explicativa para a questão 3
# RespostaExplicacao.objects.create(
#     questao=questao3,
#     texto='O comando correto para iniciar um projeto Django é "django-admin startproject".'
# )

# # Criar pontuação
# # usuario = User.objects.create_user(username='testuser', password='testpass')
# # Pontuacao.objects.create(
# #     usuario=usuario,
# #     quiz=quiz,
# #     pontuacao=10
# # )

