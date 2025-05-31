from django.urls import path
from . import views

urlpatterns = [
    # Listar disiciplinas
    path('disciplinas/', views.disciplinas_lista, name='disciplinas_list'),
    
    # Listar quizzes da disiciplina
    path('disciplinas/<int:disciplina_id>/quizzes/', views.disciplina_quizzes, name='disciplina_quizzes'),

    # Listar questão(ões) de um quiz + Receber resposta do aluno
    path('quizzes/<int:quiz_id>/questoes/', views.quiz_questoes, name='quizzes_detail'),
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/', views.quiz_questoes, name='quizzes_detail'),

    # Certificado
    path('certificados/<str:codigo>/', views.certificados, name='certificado'),


]


