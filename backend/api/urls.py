from django.urls import path
from .views import *

urlpatterns = [
    # rota inicial - teste api
    path('', IndexView.as_view(), name='index'),

    # teste - saiu da pagina
    # path('saiu-da-pagina/', SaiuDaPaginaView.as_view(), name='saiu-da-pagina'),

    # Listar disiciplinas
    path('disciplinas/', DisciplinaListView.as_view(), name='disciplinas_list'),

    # Listar quizzes
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),

    # Listar questão(ões) de um quiz
    path('quizzes/<int:quiz_id>/questoes/', QuizQuestoesListView.as_view(), name='quizzes_questoes'),

    # Verificar se o aluno pode fazer o quiz
    path('quizzes/<int:quiz_id>/aluno-pode-fazer/', AlunoPodeFazerQuizView.as_view(), ),
    
    # Informações do quiz
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz_detail'),

    # Iniciar quiz
    path('quizzes/<int:quiz_id>/iniciar/', IniciarQuizView.as_view(), name='iniciar_quiz'),

    # # Desistir do quiz
    path('quizzes/<int:quiz_id>/desistir/', DesistirQuizView.as_view(), name='desistir_quiz'),

    # # Concluir quiz
    path('quizzes/<int:quiz_id>/concluir/', ConcluirQuizView.as_view(), name='concluir_quiz'),

    # Enviar resposta do aluno
    path('quizzes/<int:quiz_id>/questoes/<int:questao_id>/responder/', ResponderQuestaoView.as_view(), name='responder_questao_detail'),

    # Obter todas as respostas corretas (gabarito)
    path('quizzes/<int:quiz_id>/questoes/respostas-corretas/', ListRespostasQuestoesView.as_view(), name='resposta_questao'),

    # Respostas do aluno no ultimo quiz
    path('quizzes/<int:quiz_id>/respostas-ultimo-quiz/', ListRespostaaAlunoQuiz.as_view(), name='respostas-ultimo-quiz'),

    # Emblemas
    path('emblemas/', ListEmblemasView.as_view(), name='emblemas'),

    # Emblemas do aluno
    path('emblemas/aluno/', ListEmblemasUserView.as_view(), name='emblemas-aluno'),

    # estatisticas -> para obter dados de quizzes e nome da disciplina
    path('tentativas/', ListTentativasView.as_view(), name='tentativas'),

    # obter status de um quiz -> tentativa
    path('tentativas/quiz/<int:quiz_id>/', TentativaStatusQuizView.as_view(), name='tentativas-status-quiz'),

]
