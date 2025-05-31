from django.urls import path
from . import views

urlpatterns = [
    # Listar disiciplinas
    path('disciplinas/', views.disciplinas_lista, name='disciplinas_list'),
    
    # Listar quizzes da disiciplina
    path('disciplinas/<int:disciplina_id>/quizzes/', views.disciplina_quizzes, name='disciplina_quizzes'),

    # Listar questões de um quiz
    path('quizzes/<int:quiz_id>/questoes/', views.quiz_questoes, name='quizzes_detail'),
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/', views.quiz_questoes, name='quizzes_detail'),

    # Listar respostas de uma questão
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/resposta/', views.questao_resposta, name='questoes_respostas'),

    # Certificado
    path('certificados/<str:codigo>/', views.certificados, name='certificado'),
]


