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
    """
    View para iniciar um quiz
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        resposta = aluno_pode_fazer_quiz(quiz, aluno)

        if resposta['detail'] != "OK":
            return Response(resposta, status=status.HTTP_200_OK)

        # verificar se existe tentativa NÃO concluída deste quiz
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz=quiz
        ).exclude(status_quiz="Concluído").last()

        if tentativa:
            return Response(
                {"detail": "Este quiz já foi iniciado e ainda não foi concluído"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # contar tentativas anteriores para gerar num_tentativa
        total_tentativas = Tentativa.objects.filter(aluno=aluno, quiz=quiz).count()
        proxima_tentativa = total_tentativas + 1

        # criar nova tentativa
        Tentativa.objects.create(
            aluno=aluno,
            quiz=quiz,
            status_quiz="Iniciado",
            num_tentativa=proxima_tentativa
        )

        return Response({"detail": "ok"}, status=status.HTTP_201_CREATED)

# ====================================================
# Desistir de um quiz
# ====================================================
class DesistirQuizView(APIView):
    """
    View para desisir de um quiz
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        resposta = aluno_pode_fazer_quiz(quiz, aluno)

        if resposta['detail'] != "OK":
            return Response(resposta, status=status.HTTP_200_OK)

        # obter a tentativa
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz=quiz
        ).exclude(status_quiz="Concluído").last()

        tentativa.status_quiz = "Desistido"
        tentativa.save()

        # excluir todas as respostas associadas a esta tentativa
        RespostaAluno.objects.filter(tentativa=tentativa).delete()

        return Response(
            {"detail": "Tentativa marcada como desistida com sucesso"},
            status=status.HTTP_200_OK
        )
    
# ====================================================
# Concluir um quiz
# ====================================================
class ConcluirQuizView(APIView):
    """
    View para concluir um quiz
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        aluno = get_object_or_404(CustomUser, user=request.user)

        resposta = aluno_pode_fazer_quiz(quiz, aluno)
        if resposta['detail'] != "OK":
            return Response(resposta, status=status.HTTP_200_OK)

        # tentativa ativa
        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz=quiz
        ).exclude(status_quiz="Concluído").last()

        if not tentativa:
            return Response(
                {"detail": "Nenhuma tentativa ativa encontrada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # buscar respostas do aluno
        respostas_aluno = RespostaAluno.objects.filter(
            aluno=aluno,
            tentativa=tentativa
        )

        total_questoes = quiz.questoes.count()

        # se não respondeu nada
        if respostas_aluno.count() == 0:
            return Response(
                {"detail": "Você não respondeu nenhuma questão."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # calcular acertos
        num_acertos = 0

        for resposta in respostas_aluno:
            resposta_correta = RespostaQuestao.objects.get(
                questao=resposta.questao
            )
            if resposta_correta.alternativa_id == resposta.alternativa_id:
                num_acertos += 1

        # porcentagem real com base nas questões do quiz
        porcentagem = (num_acertos / total_questoes) * 100

        # salvar na tentativa
        tentativa.pontuacao = porcentagem
        tentativa.aprovado = porcentagem >= 70
        tentativa.status_quiz = "Concluído"
        tentativa.save()

        # gerar certificado se for aprovado
        if quiz.nivel == "Avançado" and tentativa.aprovado:
            data = {
                "aluno": request.user.username,
                "disciplina": quiz.disciplina.nome,
                "acertos": num_acertos,
            }
            gerar_certificado_no_banco(data)
            print('>_ certificado gerado!!!')

        return Response(
            {
                "detail": "Quiz concluído com sucesso",
                "acertos": num_acertos,
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
            # "correto": alternativa.correta,
            "detail": "Resposta registrada com sucesso."
        }

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

        tentativa = Tentativa.objects.filter(
            aluno=aluno,
            quiz=quiz
        ).first()

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

# ================================================================================================
#                                           Área Admin
# ================================================================================================

# # ADMIN: Criar uma disciplina
# class DisciplinaCreateView(APIView):
#     """
#     View para criar uma disciplina
#     """

#     permission_classes = [IsAuthenticated, IsAdminQuizzesPermission]

#     def post(self, request):
#         serializer = DisciplinaSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(
#                 {"errors": serializer.errors},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer.save()
#         return Response(
#             {"message": "Disciplina criada com sucesso!"},
#             status=status.HTTP_201_CREATED
#         )
    

# # ADMIN: Editar/excluir uma disciplina
# class DisciplinaDetailView(APIView):
#     """
#     ADMIN: View para editar e excluir uma disiciplina
#     """

#     permission_classes = [IsAuthenticated, IsAdminQuizzesPermission]

#     def get_object(self, id):
#         return get_object_or_404(Disciplina, id=id)

#     def get(self, request, id):
#         disciplina = self.get_object(id)
#         serializer = DisciplinaSerializer(disciplina)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         disciplina = self.get_object(id)
#         serializer = DisciplinaSerializer(disciplina, data=request.data, partial=False)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Disciplina atualizada com sucesso!"},
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             {"errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, id):
#         disciplina = self.get_object(id)
#         disciplina.delete()
#         return Response(
#             {"message": "Disciplina excluída com sucesso!"},
#             status=status.HTTP_204_NO_CONTENT
#         )

# # ADMIN: POST quizzes
# class QuizCreateView(APIView):
#     """
#     ADMIN: View para criar um quiz
#     """

#     permission_classes = [IsAuthenticated, IsAdminQuizzesPermission]

#     def post(self, request):
#         serializer = QuizSerializer(data=request.data)
#         if serializer.is_valid():
#             # Cria o Quiz
#             quiz = serializer.save()

#             # Agora cria as questões e relacionadas
#             questoes_data = request.data.get("questoes", [])
#             for questao_data in questoes_data:
#                 # criar a questão
#                 descricao = questao_data.get('descricao', '')
#                 questao = Questao.objects.create(quiz=quiz, descricao=descricao)
#                 print(f'--- Questao criada: {questao}')

#                 # criar as alternativas
#                 alternativas_data = questao_data.get('alternativas', [])
#                 for texto in alternativas_data:
#                     Alternativa.objects.create(questao=questao, texto=texto)
#                     print(f'--- Alternativa criada: {texto}')
                
#                 # salva a resposta correta
#                 resposta_data = questao_data.get('resposta_correta', '')
#                 explicacao = questao_data.get('explicacao', '')
#                 alternativa_correta = Alternativa.objects.filter(
#                     questao=questao, texto=resposta_data
#                 ).first()
#                 if alternativa_correta:
#                     Resposta.objects.create(
#                         questao=questao,
#                         alternativa=alternativa_correta,
#                         explicacao=explicacao
#                     )
#                     print(f'--- Resposta correta criada: {resposta_data}')

#             return Response(
#                 {"message": "Quiz criado com sucesso!"},
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
# # ADMIN: GET/PUT/DELETE quiz por ID
# class QuizDetailAPIView(APIView):
#     """
#     ADMIN: View para obter/atualizar/excluir um quiz
#     """
    
#     permission_classes = [IsAuthenticated, IsAdminQuizzesPermission]

#     def get(self, request, id):
#         quiz = get_object_or_404(Quiz, id=id)
#         serializer = QuizSerializer(quiz)
#         return Response(serializer.data)
    
#     def patch(self, request, id):
#         quiz = get_object_or_404(Quiz, id=id)
#         serializer = QuizSerializer(quiz, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Quiz atualizado com sucesso!"},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, id):
#         quiz = get_object_or_404(Quiz, id=id)
#         quiz.delete()
#         return Response(
#                 {"message": "Quiz excluído com sucesso!"},
#                 status=status.HTTP_204_NO_CONTENT
#             )    

# # ADMIN: GET/POST questão
# class QuestaoCreateView(APIView):
#     """
#     ADMIN: View para criar e listar questões
#     """

#     permission_classes = [IsAuthenticated, IsAdminQuizzesPermission]

#     def get(self, request):
#         questoes = Questao.objects.all()
#         serializer = QuestaoSerializer(questoes, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = QuestaoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ADMIN: GET/PATCH/DELETE questão por ID
# class QuestoesPatchDeleteView(APIView):
#     """
#     ADMIN: View para obter/atualizar/excluir uma questão
#     """
    
#     permission_classes = [IsAuthenticated, IsAdminQuizzesPermission]

#     def get(self, request, quiz_id, questao_id):
#         questao = get_object_or_404(Questao, id=questao_id, quiz__id=quiz_id)
#         serializer = QuestaoSerializer(questao)
#         return Response(serializer.data)

#     def patch(self, request, quiz_id, questao_id):
#         questao = get_object_or_404(Questao, id=questao_id, quiz__id=quiz_id)
#         serializer = QuestaoSerializer(questao, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, quiz_id, questao_id):
#         questao = get_object_or_404(Questao, id=questao_id, quiz__id=quiz_id)
#         questao.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class QuestaoDetailView(APIView):
#     """
#     View para:
#         - Obter detalhes de uma questão específica de um quiz
#         - Registrar a resposta do aluno nesta questão.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request, quiz_id, questao_id):
#         questao = get_object_or_404(Questao, quiz_id=quiz_id, id=questao_id)
#         serializer = QuestaoSerializer(questao)
#         return Response(serializer.data)


# class ResponderQuestaoView(APIView):
#     """
#     View para enviar a resposta do aluno para uma questão
#     """
    
#     permission_classes = [IsAuthenticated]

#     def post(self, request, quiz_id, questao_id):
#         print("enviou resposta -----")
#         desempenho = Desempenho.objects.filter(aluno=request.user.aluno).last()

#         if desempenho is None:
#             return Response({
#                 'detail': 'Quiz não iniciado!!!'
#             })

#         alternativa_id = request.data.get('alternativa_id')
#         if not alternativa_id:
#             return Response({'detail': '"alternativa_id" não informado'}, status=status.HTTP_400_BAD_REQUEST)

#         quiz = get_object_or_404(Quiz, id=quiz_id)
#         questao = get_object_or_404(Questao, id=questao_id)
#         alternativa = get_object_or_404(Alternativa, id=alternativa_id)

#         # registrar tentativa
#         existe_tentativa_com_esse_desempenho = Tentativa.objects.filter(
#             aluno=request.user.aluno,
#             desempenho=desempenho
#         ).exists()

#         if existe_tentativa_com_esse_desempenho:
#             print('Questão já respondida')
#             return Response({'detail': 'Questão já respondida'}, status=status.HTTP_403_FORBIDDEN)

#         resposta_aluno, created = RespostaAluno.objects.get_or_create(
#             desempenho=desempenho,
#             questao=questao,
#             defaults={
#                 'alternativa': alternativa
#             }
#         )

#         resposta_aluno.alternativa = alternativa
#         resposta_aluno.save()

#         res_questao = get_object_or_404(Resposta, questao=questao)
#         correto = res_questao.alternativa == alternativa
        
#         print('> Questão')
#         print(f'[{questao.id}] {questao.descricao}')
#         print()
#         print('> Respostas')
#         print('RC:', res_questao.alternativa)
#         print('IM:', alternativa)

#         if correto:
#             desempenho = Desempenho.objects.filter(
#                 aluno=request.user.aluno,
#                 disciplina=quiz.disciplina,
#                 quiz=quiz
#             ).last()

#             if not desempenho:
#                 desempenho = Desempenho.objects.create(
#                     aluno=request.user.aluno,
#                     disciplina=quiz.disciplina,
#                     quiz=quiz,
#                     num_acertos=0
#                 )

#             desempenho.num_acertos += 1
#             desempenho.save()
#             print(f"[DEBUG] {'Criado' if created else 'Atualizado'} desempenho: {desempenho.num_acertos}")
#         else:
#             print("[DEBUG] Alternativa incorreta.")

#         resp = {
#             'detail': 'Respondida!',
#             "correto": correto,
#             "id": questao_id,
#             "questao": questao.descricao,
#             "alternativa": alternativa.texto,
#             "explicacao": res_questao.explicacao
#         }
#         return Response(resp)


# class RespostaQuestaoView(APIView):
#     """
#     View para retornar a resposta correta de uma questão específica de um quiz.
#     """

#     def get(self, request, quiz_id, questao_id):
#         if quiz_id and questao_id:
#             questao = get_object_or_404(Questao, quiz_id=quiz_id, id=questao_id)
#             print('quiz.respostas')
#             print(resposta := questao.resposta)
#             serializer = RespostaSerializer(resposta)
#             return Response({'detail': serializer.data})
#         else:
#             return Response({'detail': 'ID da questao e do quiz não fornecido!!'})

# class IniciarQuizView(APIView):
#     """
#     Iniciar um quiz e registrar o desempenho.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request, quiz_id):

#         quiz = get_object_or_404(Quiz, id=quiz_id)

#         Desempenho.objects.create(
#             aluno=request.user.aluno,
#             quiz=quiz,
#             disciplina=quiz.disciplina,
#         )

#         data = {
#             "detail": "ok"
#         }
#         return Response(data, status=status.HTTP_201_CREATED)
    

# class DesistirQuizView(APIView):
#     """
#     Excluir os objetos "RespostaAluno" e "Desempenho" relacionados ao usuário e ao quiz.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request, quiz_id):
#         if not quiz_id:
#             return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

#         quiz = get_object_or_404(Quiz, id=quiz_id)

#         desempenho = Desempenho.objects.filter(
#             aluno=request.user.aluno,
#             quiz=quiz,
#             disciplina=quiz.disciplina,
#             concluiu_quiz=False
#         ).last()

#         # verifica se iniciou o quiz
#         if not desempenho:
#             return Response({"error": "Quiz não iniciado!"}, status=status.HTTP_404_NOT_FOUND)

#         print('>_ desisitr -----')
#         print(desempenho)
#         desempenho.concluiu_quiz = True
#         desempenho.save()

#         # registrar tentativa
#         Tentativa.objects.create(
#             aluno=request.user.aluno,
#             desempenho=desempenho,
#             concluiu_quiz=False
#         )
        
#         # excluir as questões respondidas
#         RespostaAluno.objects.filter(desempenho=desempenho).delete()

#         return Response({"detail": "Você desistiu do quiz!"})


# def calcular_e_salvar_pontuacao(aluno, nivel, acertos, tentativa, salvar_no_banco=False):

#     print('>_ Chamou método `calcular_e_salvar_pontuacao`')

#     NIVEIS_PONTOS = {
#         "Iniciante": 10,
#         "Intermediário": 15,
#         "Avançado": 20,
#     }

#     PESO_BASE = NIVEIS_PONTOS[nivel]
#     desconto = tentativa * 2
#     PESO_PONTUACAO = min(PESO_BASE - desconto, PESO_BASE)

#     pontos_novos = acertos * PESO_PONTUACAO

#     if salvar_no_banco:
#         pontuacao, created = Pontuacao.objects.get_or_create(
#             aluno=aluno,
#             defaults={'pontos': pontos_novos}
#         )

#         if not created:
#             pontuacao.pontos += pontos_novos
#             pontuacao.save()
        
#         return pontuacao, True

#     return pontos_novos, False


# class ConcluirQuizView(APIView):
#     """
#     Concluir o quiz e mostrar o desempenho do usuário.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request, quiz_id):
#         if not quiz_id:
#             return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

#         quiz = get_object_or_404(Quiz, id=quiz_id)

#         print('Desempenho -----------')
#         print(request.user.aluno)
#         desempenho = Desempenho.objects.filter(
#             aluno=request.user.aluno,
#             quiz=quiz,
#             disciplina=quiz.disciplina,
#             concluiu_quiz=False
#         ).last()
        
#         # verifica se iniciou o quiz
#         if not desempenho:
#             return Response({"error": "Quiz não iniciado!"}, status=status.HTTP_404_NOT_FOUND)
        
#         # concluir quiz
#         desempenho.concluiu_quiz = True
#         desempenho.save()

#         data = {
#             "aluno": request.user.username,
#             "disciplina": quiz.disciplina.nome,
#             "acertos": desempenho.num_acertos,
#         }

#         acertos = desempenho.num_acertos / quiz.questoes.count()
#         print('+--------------------+')
#         print(f'>_ acertos: {(acertos*100):.2f}%')
#         print('+--------------------+')

#         if acertos == 1:
#             """
#             Conceder emblema de 'Quiz 100%'
#             """
#             EmblemaUser.objects.get_or_create(
#                 aluno=request.user.aluno,
#                 emblema__nome="Quiz 100%",
#             )
#             print('100% do quiz -------')

#         # pelo menos 70/80%
#         atingiu_minimo = acertos >= 0.6
#         if atingiu_minimo:
                           
#             if quiz.nivel == "Avançado":
#                 """
#                 Verifica se o usuário já possui o emblema de "Especialista em Disciplina
#                 """
#                 emblema, _ = EmblemaUser.objects.get_or_create(
#                     aluno=request.user.aluno,
#                     emblema__nome="Especialista em Disciplina"
#                 )
#                 gerar_certificado_no_banco(data)

#             elif quiz.nivel == "Intermediário":
#                 emblema, _ = EmblemaUser.objects.get_or_create(
#                     aluno=request.user.aluno,
#                     emblema__nome="Primeiro Nível Intermediário"
#                 )
            
#             elif quiz.nivel == "Iniciante":
#                 """
#                 Verifica se o usuário já possui o emblema de "Primeiro Quiz".
#                 """
#                 emblema, _ = EmblemaUser.objects.get_or_create(
#                     aluno=request.user.aluno,
#                     emblema__nome="Primeiro Quiz"
#                 )
#                 print('1st emblema -----')

            
#         # calcular pontuação
#         print('>_ calcular pontuação')
        
#         aluno = request.user.aluno
#         pontuacao, eh_objeto = calcular_e_salvar_pontuacao(
#             aluno,
#             quiz.nivel,
#             data['acertos'],
#             Tentativa.objects.filter(aluno=aluno).count() + 1,
#             atingiu_minimo
#         )

#         if eh_objeto:
#             data['pontos'] = pontuacao.pontos
#         else:
#             data['pontos'] = pontuacao
        
#         # registrar tentativa
#         Tentativa.objects.create(
#             aluno=request.user.aluno,
#             desempenho=desempenho,
#             concluiu_quiz=True
#         )

#         return Response(data)


# class UltimosDesempenhosView(APIView):
#     """
#     Retorna os 3 últimos desempenhos do usuário autenticado.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         desempenhos = Desempenho.objects.filter(user=request.user).order_by('-id')[:3]
#         data = [
#             {
#                 'quiz': d.quiz.nivel,
#                 'disciplina': d.quiz.disciplina.nome,
#                 'acertos': d.num_acertos,
#                 'total_questoes': d.quiz.questoes.count(),
#             }
#             for d in desempenhos
#         ]
#         return Response(data)


# class RespostaUltimoQuiz(APIView):
#     """
#     Retorna todas as respostas do aluno para um quiz específico
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request, quiz_id):
#         quiz = get_object_or_404(Quiz, id=quiz_id)
#         num_quesotes_quiz = quiz.questoes.count()
#         print('> num_quesotes_quiz:', num_quesotes_quiz)
#         respostas = RespostaAluno.objects.filter(
#             desempenho__aluno=request.user.aluno,
#             questao__quiz__id=quiz_id
#         ).order_by('-id')[:num_quesotes_quiz]

#         serializer = RespostaAlunoSerializer(respostas, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class FeedbackView(APIView):
#     permission_classes = [AllowAny]
#     """
#     View para receber feedbacks dos usuários.
#     """

#     def post(self, request):
#         serializer = FeedbackSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)

#         serializer.save()

#         email = request.data.get('email')
#         assunto_admin = request.data.get('assunto')
#         mensagem_admin = request.data.get('mensagem')

#         if not email or not assunto_admin or not mensagem_admin:
#             return Response({'error': 'Campos obrigatórios ausentes'}, status=400)

#         # Email para o usuário
#         send_mail(
#             'Feedback enviado!!!',
#             'Seu feedback foi enviado!! Aguarde a resposta dos administradores!',
#             settings.EMAIL_HOST_USER,
#             [email]
#         )

#         # Email para os administradores
#         send_mail(
#             f'Novo feedback: {assunto_admin}',
#             f'Mensagem: {mensagem_admin}\nEmail do remetente: {email}',
#             settings.EMAIL_HOST_USER,
#             [settings.EMAIL_HOST_USER]
#         )

#         return Response({'detail': 'Feedback enviado com sucesso!'})
    
# class EmblemaListView(APIView):
#     """
#     View para listar os emblemas do usuário.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         emblemas = Emblema.objects.values("nome", "descricao", "logo").distinct()
#         return Response(emblemas)
    

# class EmblemaUserListView(APIView):
#     """
#     View para listar os emblemas do usuário.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request, username=None):
#         aluno = get_object_or_404(CustomUser, user__username=username)
#         emblemas = EmblemaUser.objects.filter(aluno=aluno)
#         serializer = EmblemaUserSerializer(emblemas, many=True)
#         return Response(serializer.data)

# class PontuacaoTop3ListView(APIView):
#     """
#     View para listar o top 3
#     """
#     def get(self, request):
#         pontuacoes = Pontuacao.objects.all().order_by('-pontos')[:3]
#         serializer = PontuacaoSerializer(pontuacoes, many=True)
#         return Response(serializer.data)


# class PontuacaoListView(APIView):
#     """
#     View para listar as pontuações.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request, username=None):
#         if username:
#             aluno = get_object_or_404(CustomUser, user__username=username)
#             pontuacao = get_object_or_404(Pontuacao, aluno=aluno)
#             serializer = PontuacaoSerializer(pontuacao)
#             return Response(serializer.data)
        
#         pontuacoes = Pontuacao.objects.all().order_by('-pontos')
#         serializer = PontuacaoSerializer(pontuacoes, many=True)
#         return Response(serializer.data)

    
