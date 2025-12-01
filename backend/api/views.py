from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdminQuizzesPermission
from certificado.views import gerar_certificado_no_banco
from .models import CustomUser, Tentativa, Quiz, Questao, Disciplina, Alternativa, RespostaAluno, RespostaQuestao, Emblema, EmblemaUser
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, QuestaoRespostaSerializer, RespostaAlunoSerializer, EmblemaSerializer, EmblemaUserSerializer, TentativaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import random
from django.core.mail import send_mail
from django.conf import settings

# ====================================================
# Rota teste da API
# ====================================================
class IndexView(APIView):
    """
    View para testar conexão com a API
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({'message': 'API ON!!!'})

# ====================================================
# Rota teste da API - saiu de uma página (de quiz iniciado)
# ====================================================
class SaiuDaPaginaView(APIView):
    """
    View para testar conexão com a API
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f'>_ usuário {request.user.username} saiu da página!!!')
        return JsonResponse({'detail': 'Saiu da página!!!'})

# ================================================================================================
#                                           Área aluno
# ================================================================================================

# - Listar disiplinas
# - Listar quizzes
# - Listar as questões de um quiz (se puder fazer o quiz)
# - Verificar se o aluno pode fazer o quiz
# - Obter informações do quiz
# - Iniciar um quiz
# - Desistir de um quiz
# - Concluir um quiz
# - Enviar resposta do aluno
# - Obter todas as respostas corretas (gabarito)
# - Obter todas as respostas do aluno

# ====================================================
# Listar disciplinas
# ====================================================
class DisciplinaListView(APIView):
    """
    View para listar todas as disciplinas disponíveis.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        disciplinas = Disciplina.objects.all()
        serializer = DisciplinaSerializer(disciplinas, many=True)
        return Response(serializer.data)

# ====================================================
# Listar quizzes
# ====================================================
class QuizListView(APIView):
    """
    View para listar todos os quizzes disponíveis.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
# ====================================================
# Listar as questões de um quiz
# ====================================================
class QuizQuestoesListView(APIView):
    """
    Veirficar se atingiu pelo 70% de acertos no nível anterior
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questoes = list(Questao.objects.filter(quiz=quiz))
        random.shuffle(questoes)
        questoes_aleatorias = questoes[:10]
        
        serializer = QuestaoSerializer(questoes_aleatorias, many=True)
        return Response(serializer.data)

# ====================================================
# Verificar se o aluno pode fazer o quiz
# ====================================================

# Método para verificar se o aluno pode fazer
def aluno_pode_fazer_quiz(quiz, aluno):
    # ----------- Avançado -----------
    if quiz.nivel == "Avançado":
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz__nivel="Intermediário",
            aprovado=True,
            status_quiz="Concluído"
        ).first()

        if not tentativa:
            return {'detail': 'Você não pode fazer o nível Avançado!'}

    # ----------- Intermediário -----------
    elif quiz.nivel == "Intermediário":
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz__nivel="Iniciante",
            aprovado=True,
            status_quiz="Concluído"
        ).first()

        print('tentativa INT:', tentativa)

        if not tentativa:
            return {'detail': 'Você não pode fazer o nível Intermediário!'}

    return {"detail": "OK"}


# View
class AlunoPodeFazerQuizView(APIView):
    """
    Verificar se o aluno pode fazer o quiz
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)
        print(f'Quiz: {quiz.titulo}')
        resposta = aluno_pode_fazer_quiz(quiz, aluno)
        return Response(resposta, status=status.HTTP_200_OK)

# ====================================================
# Obter informações do quiz
# ====================================================
class QuizDetailView(APIView):
    """
    View para obter detalhes de um quiz específico.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

# ====================================================
# Iniciar um quiz
# ====================================================
class IniciarQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        print("\n===== INICIAR QUIZ =====")

        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        print(f"> Usuário: {aluno.user.username} (ID {aluno.id})")
        print(f"> Quiz: {quiz.titulo} | Disciplina: {quiz.disciplina.nome} | Nível: {quiz.nivel}")

        resposta = aluno_pode_fazer_quiz(quiz, aluno)
        print(f"> Validação do aluno: {resposta}")

        if resposta["detail"] != "OK":
            print("> BLOQUEADO: aluno não pode fazer o quiz.")
            return Response(resposta, status=status.HTTP_200_OK)

        # ⛔ Bloqueia apenas tentativas em andamento (Iniciado)
        tentativa_aberta = (
            Tentativa.objects
            .filter(aluno=aluno, quiz=quiz, status_quiz="Iniciado")
            .order_by("-id")
            .first()
        )

        print("> Tentativa em aberto encontrada?", "SIM" if tentativa_aberta else "NÃO")

        if tentativa_aberta:
            print(f"> BLOQUEADO: tentativa ID {tentativa_aberta.id} ainda está Iniciada.")
            return Response(
                {"detail": "Este quiz já foi iniciado e ainda não foi concluído"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # gerar número da tentativa
        total = Tentativa.objects.filter(aluno=aluno, quiz=quiz).count()
        proxima = total + 1
        print(f"> Total tentativas anteriores: {total}")
        print(f"> Próxima tentativa: {proxima}")

        nova = Tentativa.objects.create(
            aluno=aluno,
            quiz=quiz,
            status_quiz="Iniciado",
            num_tentativa=proxima
        )

        print(f"> TENTATIVA CRIADA! ID {nova.id}")
        print("===== FIM INICIAR QUIZ =====\n")

        return Response({"detail": "ok"}, status=status.HTTP_201_CREATED)

# ====================================================
# Desistir de um quiz
# ====================================================
# ====================================================
# Desistir de um quiz
# ====================================================
class DesistirQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        print("\n===== DESISTIR QUIZ =====")

        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        print(f"> Usuário: {aluno.user.username} (ID {aluno.id})")
        print(f"> Quiz: {quiz.titulo}")

        resposta = aluno_pode_fazer_quiz(quiz, aluno)
        print("> Validação:", resposta)

        if resposta["detail"] != "OK":
            return Response(resposta, status=status.HTTP_200_OK)

        # busca tentativa ativa
        tentativa = (
            Tentativa.objects
            .filter(aluno=aluno, quiz=quiz, status_quiz="Iniciado")
            .order_by("-id")
            .first()
        )

        print("> Tentativa ativa encontrada?", "SIM" if tentativa else "NÃO")

        if not tentativa:
            print("> ERRO: Nenhuma tentativa em andamento para desistir.")
            return Response(
                {"detail": "Nenhuma tentativa ativa para desistir."},
                status=status.HTTP_400_BAD_REQUEST
            )

        tentativa.status_quiz = "Desistido"
        tentativa.save()

        print(f"> Tentativa ID {tentativa.id} marcada como DESISTIDA.")

        # excluir respostas dessa tentativa
        RespostaAluno.objects.filter(tentativa=tentativa).delete()
        print("> Respostas removidas.")

        print("===== FIM DESISTIR QUIZ =====\n")

        return Response({"detail": "Você desistiu do quiz."}, status=status.HTTP_200_OK)

# ====================================================
# Concluir um quiz
# ====================================================
class ConcluirQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        print("\n===== CONCLUIR QUIZ =====")

        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        print(f"> Usuário: {aluno.user.username} (ID {aluno.id})")
        print(f"> Quiz: {quiz.titulo}")

        resposta = aluno_pode_fazer_quiz(quiz, aluno)
        print("> Validação:", resposta)

        if resposta["detail"] != "OK":
            return Response(resposta, status=status.HTTP_200_OK)

        # busca tentativa ativa
        tentativa = (
            Tentativa.objects
            .filter(aluno=aluno, quiz=quiz, status_quiz="Iniciado")
            .order_by("-id")
            .first()
        )

        print("> Tentativa ativa encontrada?", "SIM" if tentativa else "NÃO")

        if not tentativa:
            return Response(
                {"detail": "Nenhuma tentativa ativa encontrada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        respostas_aluno = RespostaAluno.objects.filter(
            aluno=aluno,
            tentativa=tentativa
        )

        if respostas_aluno.count() == 0:
            return Response(
                {"detail": "Você não respondeu nenhuma questão."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_questoes = quiz.questoes.count()
        acertos = 0

        # CORREÇÃO -> obter alternativa correta
        for resposta in respostas_aluno:
            alternativa_correta = (
                RespostaQuestao.objects
                .filter(questao=resposta.questao)
                .first()
            ).alternativa

            if alternativa_correta and alternativa_correta.id == resposta.alternativa.id:
                acertos += 1

        porcentagem = (acertos / total_questoes) * 100

        tentativa.pontuacao = porcentagem
        tentativa.aprovado = porcentagem >= 70
        tentativa.status_quiz = "Concluído"
        tentativa.save()

        print(f"> Pontuação: {porcentagem}% | Aprovado: {tentativa.aprovado}")

        # Emblema
        if tentativa.aprovado:
            print("> Aprovado: verificando emblemas...")
            emblema = Emblema.objects.filter(
                disciplina=quiz.disciplina,
                nivel=quiz.nivel
            ).first()

            if emblema:
                EmblemaUser.objects.create(aluno=aluno, emblema=emblema)
                print("> Emblema concedido!")

        # Certificado (somente nível Avançado)
        if tentativa.aprovado and quiz.nivel == "Avançado":
            data = {
                "aluno": request.user.username,
                "disciplina": quiz.disciplina.nome,
                "acertos": acertos,
            }
            gerar_certificado_no_banco(data)
            print("> Certificado gerado!")

        print("===== FIM CONCLUIR QUIZ =====\n")

        return Response(
            {
                "detail": "Quiz concluído com sucesso",
                "acertos": acertos,
                "total_questoes": total_questoes,
                "porcentagem": round(porcentagem, 2),
                "aprovado": tentativa.aprovado
            },
            status=status.HTTP_200_OK
        )

# ====================================================
# Enviar resposta do aluno
# ====================================================
class ResponderQuestaoView(APIView):
    """
    View para enviar a resposta do aluno
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, quiz_id, questao_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questao = get_object_or_404(Questao, id=questao_id)
        alternativa_id = request.data.get('alternativa_id')
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        # pegar a última tentativa não concluída
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz=quiz
        ).exclude(status_quiz="Concluído").last()

        if not tentativa:
            return Response(
                {"detail": "Nenhuma tentativa ativa encontrada para este quiz."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # verificar se já respondeu esta questão na tentativa atual
        resposta_existente = RespostaAluno.objects.filter(
            aluno=aluno,
            tentativa=tentativa,
            questao=questao
        ).first()

        if resposta_existente:
            return Response(
                {
                    "questao": questao.descricao,
                    "resposta_aluno": resposta_existente.alternativa.texto,
                    "detail": "Você já respondeu esta questão nesta tentativa."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # salvar resposta do aluno
        RespostaAluno.objects.create(
            aluno=aluno,
            questao=questao,
            alternativa=alternativa,
            tentativa=tentativa
        )

        data = {
            "questao": questao.descricao,
            "resposta_aluno": alternativa.texto,
            "detail": "Resposta registrada com sucesso."
        }

        print('>_ RESPONDEUUU')
        print(data)

        return Response(
            data,
            status=status.HTTP_201_CREATED
        )

# ====================================================
# Obter todas as respostas corretas (gabarito das questões respondidas)
# ====================================================
class ListRespostasQuestoesView(APIView):
    """
    Retornar todas as questões, alternativas e resposta correta
    de um quiz específico.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        # obter a tentativa
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz=quiz,
            status_quiz='Concluído',
            aprovado=True
        ).last()

        # obter as questões respondidas pelo aluno
        respostas_aluno = RespostaAluno.objects.filter(
            aluno=aluno,
            tentativa=tentativa
        )

        if respostas_aluno.count() == 0:
            return Response(
                {"detail": "Você ainda não respondeu nenhuma questão deste quiz."},
                status=200
            )

        # retornar as questões
        questoes_ids = respostas_aluno.values_list("questao_id", flat=True)
        questoes = Questao.objects.filter(id__in=questoes_ids)
        serializer = QuestaoRespostaSerializer(questoes, many=True)
        return Response(serializer.data, status=200)

# ====================================================
# Obter todas as respostas do aluno
# ====================================================
class ListRespostaaAlunoQuiz(APIView):
    """
    View para obter as respostas do aluno no último quiz
    """

    permission_classes = [IsAuthenticated]
    
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        tentativa = (
            Tentativa.objects
            .filter(aluno=aluno, quiz=quiz, status_quiz="Concluído")
            .order_by("-id")
            .first()
        )

        # todas as respostas do aluno nesta tentativa
        respostas = RespostaAluno.objects.filter(
            aluno=aluno,
            tentativa=tentativa
        )

        serializer = RespostaAlunoSerializer(respostas, many=True)
        return Response(serializer.data, status=200)
    

# ====================================================
# Listar emblemas
# ====================================================
class ListEmblemasView(APIView):
    """
    View para listrar os emblemas
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        emblemas = Emblema.objects.all()
        serializer = EmblemaSerializer(emblemas, many=True)
        return Response(serializer.data, status=200)

# ====================================================
# Listar emblemas do aluno
# ====================================================
class ListEmblemasUserView(APIView):
    """
    View para listrar os emblemas do aluno
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        aluno = get_object_or_404(CustomUser, user=request.user)
        emblemas = EmblemaUser.objects.filter(aluno=aluno)
        serializer = EmblemaUserSerializer(emblemas, many=True)
        return Response(serializer.data, status=200)
    
# ====================================================
# Estatisticas -> para obter dados de quizzes e nome da disciplina
# ====================================================
class ListTentativasView(APIView):
    """
    View para obter dados de quizzes e nome da disciplina
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        aluno = get_object_or_404(CustomUser, user=request.user)
        tentativas = Tentativa.objects.filter(aluno=aluno)
        serializer = TentativaSerializer(tentativas, many=True)
        return Response(serializer.data, status=200)

# ====================================================
# obter status de um quiz -> tentativa
# ====================================================
class TentativaStatusQuizView(APIView):
    """
    View para obter status de um quiz -> tentativa
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        aluno = get_object_or_404(CustomUser, user=request.user)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        tentativa = (
            Tentativa.objects
            .filter(aluno=aluno, quiz=quiz)
            .exclude(status_quiz="Concluído")
            .order_by("-id")
            .first()
        )
        return Response({"status": tentativa.status_quiz})

# ================================================================================================
#                                           Área Admin
# ================================================================================================

