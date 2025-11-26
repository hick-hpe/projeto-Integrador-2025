from django.urls import path
from .views import *

urlpatterns = [
    # rota inicial - teste api
    path('', IndexView.as_view(), name='index'),

    # Listar disiciplinas
    path('disciplinas/', DisciplinaListView.as_view(), name='disciplinas_list'),
    
    # Listar quizzes da disiciplina
    path('disciplinas/<int:disciplina_id>/quizzes/', DisciplinaQuizzesView.as_view(), name='disciplina_quizzes'),

    # Listar questão(ões) de um quiz
    path('quizzes/<int:quiz_id>/questoes/', QuizQuestoesListView.as_view(), name='quizzes_questoes'),

    # Informações do quiz
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz_detail'),

    # enviar resposta do aluno
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/responder/', ResponderQuestaoView.as_view(), name='responder_questao_detail'),

    # Listar detalhes da questão
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/', QuestaoDetailView.as_view(), name='questoes_detail'),
    
    # obter resposta correta
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/obter-resposta/', RespostaQuestaoView.as_view(), name='resposta_questao'),

    # obter todas as resposta correta
    path('quizzes/<int:quiz_id>/questoes/respostas-corretas/', ListRespostaQuestaoView.as_view(), name='resposta_questao'),

    # listar quizzes
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),

    # ============================================= CRUD - ADMIN =============================================
    # CRUD disciplina
    path('adm/disciplinas/', DisciplinaCreateView.as_view(), name='adm_disciplinas_create'),
    path('adm/disciplinas/<int:id>/', DisciplinaDetailView.as_view(), name='adm_disciplinas_detail'),

    # CRUD quiz
    path('adm/quizzes/', QuizCreateView.as_view(), name='adm_list_create_quiz'),
    path('adm/quizzes/<int:id>/', QuizDetailAPIView.as_view(), name='adm_quiz_detail'),

    # Listar/Criar questão
    path('adm/quizzes/<int:quiz_id>/questoes/', QuestaoCreateView.as_view(), name='question_create'),

    # Obter questão/Atualizar/Deletar questão
    path('adm/quizzes/<int:quiz_id>/questoes/<int:questao_id>/', QuestoesPatchDeleteView.as_view(), name='question_patch_delete'),

    # ========================================================================================================

    # Iniciar quiz
    path('quizzes/<int:quiz_id>/iniciar/', IniciarQuizView.as_view(), name='iniciar_quiz'),

    # Desistir do quiz
    path('quizzes/<int:quiz_id>/desistir/', DesistirQuizView.as_view(), name='desistir_quiz'),

    # Concluir quiz
    path('quizzes/<int:quiz_id>/concluir/', ConcluirQuizView.as_view(), name='concluir_quiz'),

    # Meus desempenhos (3 últimos) / N
    path('meus-desempenhos/', UltimosDesempenhosView.as_view(), name='ultimos_desempenhos'),

    # Respostas do aluno no ultimo quiz
    path('respostas-ultimo-quiz/<int:quiz_id>/', RespostaUltimoQuiz.as_view(), name='respostas-ultimo-quiz'),
    
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
