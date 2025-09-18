from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    # Listar disiciplinas
    path('disciplinas/', DisciplinaListView.as_view(), name='disciplinas_list'),
    
    # Listar quizzes da disiciplina
    path('disciplinas/<int:disciplina_id>/quizzes/', DisciplinaQuizzesView.as_view(), name='disciplina_quizzes'),

    # Listar questão(ões) de um quiz
    path('quizzes/<int:quiz_id>/questoes/', QuizQuestoesView.as_view(), name='quizzes_questoes'),

    # Listar detalhes da questão + Receber resposta do aluno
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/', QuestoesDetailView.as_view(), name='questoes_detail'),
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/resposta/', RespostaQuestaoView.as_view(), name='resposta_questao'),

    # Criar, atualizar e deletar quiz
    # path('quizzes/', views.crud_quiz, name='crud_quiz'),
    # path('quizzes/<int:quiz_id>/', views.crud_quiz, name='crud_quiz'),

    # Criar, atualizar e deletar questão
    # path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/', views.crud_question, name='crud_question'),

    # Iniciar quiz
    path('quizzes/<int:quiz_id>/iniciar/', IniciarQuizView.as_view(), name='iniciar_quiz'),

    # Desistir do quiz
    path('quizzes/<int:quiz_id>/desistir/', DesistirQuizView.as_view(), name='desistir_quiz'),

    # Concluir quiz
    path('quizzes/<int:quiz_id>/concluir/', ConcluirQuizView.as_view(), name='concluir_quiz'),

    # Meus desempenhos (3 últimos)
    path('meus-desempenhos/', UltimosDesempenhosView.as_view(), name='ultimos_desempenhos'),
    
    # Enviar feedbacks
    path('feedbacks/', FeedbackView.as_view(), name='feedbacks'),

    # Emblemas
    path('emblemas/user/<str:username>/', EmblemaUserListView.as_view(), name='emblemas_user'),
    path('emblemas/', EmblemaListView.as_view(), name='emblemas_list'),

    # Pontuação
    path('pontuacao/top3/', PontuacaoTop3ListView.as_view(), name='pontuacao_user'),
    path('pontuacao/<str:username>/', PontuacaoListView.as_view(), name='pontuacao_user'),
    path('pontuacao/', PontuacaoListView.as_view(), name='pontuacao_list'),

]


