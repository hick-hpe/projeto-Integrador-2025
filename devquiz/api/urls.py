from django.urls import path
from . import views

urlpatterns = [
    # Listar disiciplinas
    path('disciplinas/', views.disciplinas_lista, name='disciplinas_list'),
    
    # Listar quizzes da disiciplina
    path('disciplinas/<int:disciplina_id>/quizzes/', views.disciplina_quizzes, name='disciplina_quizzes'),

    # Listar questão(ões) de um quiz + Receber resposta do aluno
    path('quizzes/<int:quiz_id>/questoes/', views.quiz_questoes, name='quizzes_questoes'),
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/', views.questoes_detail, name='questoes_detail'),

    # Certificado
    path('certificados/<str:codigo>/', views.certificados, name='certificado'),

    # Iniciar quiz
    path('quizzes/<int:quiz_id>/iniciar/', views.iniciar_quiz, name='iniciar_quiz'),

    # Desistir do quiz
    path('quizzes/<int:quiz_id>/desistir/', views.desistir_quiz, name='desistir_quiz'),

    # Concluir quiz
    path('quizzes/<int:quiz_id>/concluir/', views.concluir_quiz, name='concluir_quiz'),
]


