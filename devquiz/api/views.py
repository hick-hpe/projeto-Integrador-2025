from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from certificado.views import gerar_certificado
from .models import Aluno, Pontuacao, Tentativa, models, Quiz, Questao, Disciplina, Alternativa, RespostaAluno, Resposta, Desempenho, Emblema
from .serializers import DisciplinaSerializer, EmblemaSerializer, PontuacaoSerializer, QuizSerializer, QuestaoSerializer, RespostaSerializer, FeedbackSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import random
from django.core.mail import send_mail
from django.conf import settings

class IndexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({'message': 'api on'})

class DisciplinaListView(APIView):
    """
    View para listar todas as disciplinas disponíveis.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        disciplinas = Disciplina.objects.all()
        serializer = DisciplinaSerializer(disciplinas, many=True)
        return Response(serializer.data)


class DisciplinaQuizzesView(APIView):
    """
    View para listar todos os quizzes de uma disciplina específica.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, disciplina_id):
        quizzes = Quiz.objects.filter(disciplina_id=disciplina_id)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class QuizQuestoesView(APIView):
    """
    Veirficar se atingiu pelo 70% de acertos no nível anterior
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        print('---- quiz ----')
        print(f'[{quiz.id}] {quiz.nivel}')

        if quiz.nivel == "Intermediário":
            desempenho = Desempenho.objects.filter(
                user=request.user,
                quiz__nivel="Iniciante",
                num_acertos__gte=7
            ).first()
            if not desempenho:
                return Response({'detail': 'Você não pode fazer o nível Intermediário!!'})
            
        elif quiz.nivel == "Avançado":
            desempenho = Desempenho.objects.filter(
                user=request.user,
                quiz__nivel="Intermediário",
                num_acertos__gte=7
            ).first()
            if not desempenho:
                return Response({'detail': 'Você não pode fazer o nível Avançado!!'})

        print('------- entregando... ------')
        questoes = list(Questao.objects.filter(quiz_id=quiz_id))
        random.shuffle(questoes)
        questoes_aleatorias = questoes[:10]
        
        serializer = QuestaoSerializer(questoes_aleatorias, many=True)
        print('--- 0 -> ini')
        return Response(serializer.data)


class QuestoesDetailView(APIView):
    """
    View para:
        - Obter detalhes de uma questão específica de um quiz
        - Registrar a resposta do aluno nesta questão.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id, questao_id):
        questao = get_object_or_404(Questao, quiz_id=quiz_id, id=questao_id)
        serializer = QuestaoSerializer(questao)
        return Response(serializer.data)

    def post(self, request, quiz_id, questao_id):
        print("enviou resposta -----")
        desempenho = Desempenho.objects.filter(aluno=request.user.aluno).last()

        if desempenho is None:
            return Response({
                'detail': 'Quiz não iniciado!!!'
            })

        alternativa_id = request.data.get('alternativa_id')
        if not alternativa_id:
            return Response({'detail': '"alternativa_id" não informado'}, status=status.HTTP_400_BAD_REQUEST)

        quiz = get_object_or_404(Quiz, id=quiz_id)
        questao = get_object_or_404(Questao, id=questao_id)
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)

        # registrar tentativa
        existe_tentativa_com_esse_desempenho = Tentativa.objects.filter(
            aluno=request.user.aluno,
            desempenho=desempenho
        ).exists()

        if existe_tentativa_com_esse_desempenho:
            print('Questão já respondida')
            return Response({'detail': 'Questão já respondida'}, status=status.HTTP_403_FORBIDDEN)

        resposta_aluno, created = RespostaAluno.objects.get_or_create(
            desempenho=desempenho,
            questao=questao,
            defaults={
                'alternativa': alternativa
            }
        )

        resposta_aluno.alternativa = alternativa
        resposta_aluno.save()

        res_questao = get_object_or_404(Resposta, questao=questao)
        correto = res_questao.alternativa == alternativa
        
        print('> Questão')
        print(f'[{questao.id}] {questao.descricao}')
        print()
        print('> Respostas')
        print('RC:', res_questao.alternativa)
        print('IM:', alternativa)

        if correto:
            desempenho = Desempenho.objects.filter(
                aluno=request.user.aluno,
                disciplina=quiz.disciplina,
                quiz=quiz
            ).last()

            if not desempenho:
                desempenho = Desempenho.objects.create(
                    aluno=request.user.aluno,
                    disciplina=quiz.disciplina,
                    quiz=quiz,
                    num_acertos=0
                )

            desempenho.num_acertos += 1
            desempenho.save()
            print(f"[DEBUG] {'Criado' if created else 'Atualizado'} desempenho: {desempenho.num_acertos}")
        else:
            print("[DEBUG] Alternativa incorreta.")

        resp = {
            'detail': 'Respondida!',
            "correto": correto,
            "id": questao_id,
            "questao": questao.descricao,
            "alternativa": alternativa.texto,
            "explicacao": res_questao.explicacao
        }
        return Response(resp)


class RespostaQuestaoView(APIView):
    """
    View para retornar a resposta correta de uma questão específica de um quiz.
    """

    def get(self, request, quiz_id, questao_id):
        if quiz_id and questao_id:
            questao = get_object_or_404(Questao, quiz_id=quiz_id, id=questao_id)
            print('quiz.respostas')
            print(resposta := questao.resposta)
            serializer = RespostaSerializer(resposta)
            return Response({'detail': serializer.data})
        else:
            return Response({'detail': 'ID da questao e do quiz não fornecido!!'})


class IniciarQuizView(APIView):
    """
    Iniciar um quiz e registrar o desempenho.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):

        quiz = get_object_or_404(Quiz, id=quiz_id)

        desempenho = Desempenho.objects.create(
            aluno=request.user.aluno,
            quiz=quiz,
            disciplina=quiz.disciplina,
        )

        data = {
            "detail": f"Você iniciou o quiz com sucesso! ID = {desempenho.id}"
        }
        return Response(data, status=status.HTTP_201_CREATED)
    

class DesistirQuizView(APIView):
    """
    Excluir os objetos "RespostaAluno" e "Desempenho" relacionados ao usuário e ao quiz.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        if not quiz_id:
            return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

        quiz = get_object_or_404(Quiz, id=quiz_id)

        desempenho = Desempenho.objects.filter(
            aluno=request.user.aluno,
            quiz=quiz,
            disciplina=quiz.disciplina,
            concluiu_quiz=False
        ).last()

        # verifica se iniciou o quiz
        if not desempenho:
            return Response({"error": "Quiz não iniciado!"}, status=status.HTTP_404_NOT_FOUND)

        print('>_ desisitr -----')
        print(desempenho)
        desempenho.concluiu_quiz = True
        desempenho.save()

        # registrar tentativa
        Tentativa.objects.create(
            aluno=request.user.aluno,
            desempenho=desempenho,
            concluiu_quiz=False
        )
        
        # excluir as questões respondidas
        RespostaAluno.objects.filter(desempenho=desempenho).delete()

        return Response({"detail": "Você desistiu do quiz!"})


def calcular_e_salvar_pontuacao(aluno, nivel, acertos, tentativa, salvar_no_banco=False):

    print('>_ Chamou método `calcular_e_salvar_pontuacao`')

    NIVEIS_PONTOS = {
        "Iniciante": 10,
        "Intermediário": 15,
        "Avançado": 20,
    }

    PESO_BASE = NIVEIS_PONTOS[nivel]
    desconto = tentativa * 2
    PESO_PONTUACAO = min(PESO_BASE - desconto, PESO_BASE)

    pontos_novos = acertos * PESO_PONTUACAO

    if salvar_no_banco:
        pontuacao, created = Pontuacao.objects.get_or_create(
            aluno=aluno,
            defaults={'pontos': pontos_novos}
        )

        if not created:
            pontuacao.pontos += pontos_novos
            pontuacao.save()
        
        return pontuacao, True

    return pontos_novos, False


class ConcluirQuizView(APIView):
    """
    Concluir o quiz e mostrar o desempenho do usuário.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        if not quiz_id:
            return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

        quiz = get_object_or_404(Quiz, id=quiz_id)

        print('Desempenho -----------')
        print(request.user.aluno)
        desempenho = Desempenho.objects.filter(
            aluno=request.user.aluno,
            quiz=quiz,
            disciplina=quiz.disciplina,
            concluiu_quiz=False
        ).last()
        
        # verifica se iniciou o quiz
        if not desempenho:
            return Response({"error": "Quiz não iniciado!"}, status=status.HTTP_404_NOT_FOUND)
        
        # concluir quiz
        desempenho.concluiu_quiz = True
        desempenho.save()

        data = {
            "aluno": request.user.username,
            "disciplina": quiz.disciplina.nome,
            "acertos": desempenho.num_acertos,
        }

        # Conceder emblema de 'Primeiro Quiz'
        Emblema.objects.get_or_create(
            aluno=request.user.aluno,
            nome="Primeiro Quiz",
            defaults={
                'descricao': 'Você completou seu primeiro quiz!',
                'logo': 'static/img/emblemas/primeiro-quiz.png'
            }
        )

        acertos = desempenho.num_acertos / quiz.questoes.count()
        print('+--------------------+')
        print(f'>_ acertos: {(acertos*100):.2f}%')
        print('+--------------------+')

        if acertos == 1:
            """
            Conceder emblema de 'Quiz 100%'
            """
            Emblema.objects.get_or_create(
                aluno=request.user.aluno,
                nome="Quiz 100%",
                defaults={
                    'descricao': 'Concluiu um quiz com 100% de acertos!',
                    'logo': 'static/img/emblemas/quiz-100.png'
                }
            )
            print('100% do quiz -------')

        # pelo menos 70/80%
        atingiu_minimo = acertos >= 0.6
        if atingiu_minimo:
                           
            if quiz.nivel == "Avançado":
                """
                Verifica se o usuário já possui o emblema de "Especialista em Disciplina
                """
                emblema, _ = Emblema.objects.get_or_create(
                    aluno=request.user.aluno,
                    nome="Especialista em Disciplina",
                    defaults={
                        'descricao': 'Concluiu com sucesso todos os quizzes de uma disciplina específica.',
                        'logo': 'static/img/emblemas/especialista-disciplina.png' # a fazer
                    }
                )
                gerar_certificado(data)

            elif quiz.nivel == "Intermediário":
                emblema, _ = Emblema.objects.get_or_create(
                    aluno=request.user.aluno,
                    nome="Primeiro Nível Avançado",
                    defaults={
                        'descricao': 'Concluiu com sucesso o primeiro quiz de nível avançado.',
                        'logo': 'static/img/emblemas/primeiro-avancado.png'
                    }
                )
            
            elif quiz.nivel == "Iniciante":
                """
                Verifica se o usuário já possui o emblema de "Primeiro Quiz".
                """
                emblema, _ = Emblema.objects.get_or_create(
                    aluno=request.user.aluno,
                    nome="Primeiro Quiz",
                    defaults={
                        'descricao': 'Concluiu o primeiro quiz na plataforma.'
                    }
                )
                print('1st emblema -----')

            
        # calcular pontuação
        print('>_ calcular pontuação')
        
        aluno = request.user.aluno
        pontuacao, eh_objeto = calcular_e_salvar_pontuacao(
            aluno,
            quiz.nivel,
            data['acertos'],
            Tentativa.objects.filter(aluno=aluno).count() + 1,
            atingiu_minimo
        )

        if eh_objeto:
            data['pontos'] = pontuacao.pontos
        else:
            data['pontos'] = pontuacao
        
        # registrar tentativa
        Tentativa.objects.create(
            aluno=request.user.aluno,
            desempenho=desempenho,
            concluiu_quiz=True
        )

        return Response(data)


class UltimosDesempenhosView(APIView):
    """
    Retorna os 3 últimos desempenhos do usuário autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        desempenhos = Desempenho.objects.filter(user=request.user).order_by('-id')[:3]
        data = [
            {
                'quiz': d.quiz.nivel,
                'disciplina': d.quiz.disciplina.nome,
                'acertos': d.num_acertos,
                'total_questoes': d.quiz.questoes.count(),
            }
            for d in desempenhos
        ]
        return Response(data)


class FeedbackView(APIView):
    permission_classes = [AllowAny]
    """
    View para receber feedbacks dos usuários.
    """

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        email = request.data.get('email')
        assunto_admin = request.data.get('assunto')
        mensagem_admin = request.data.get('mensagem')

        if not email or not assunto_admin or not mensagem_admin:
            return Response({'error': 'Campos obrigatórios ausentes'}, status=400)

        # Email para o usuário
        send_mail(
            'Feedback enviado!!!',
            'Seu feedback foi enviado!! Aguarde a resposta dos administradores!',
            settings.EMAIL_HOST_USER,
            [email]
        )

        # Email para os administradores
        send_mail(
            f'Novo feedback: {assunto_admin}',
            f'Mensagem: {mensagem_admin}\nEmail do remetente: {email}',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER]
        )

        return Response({'detail': 'Feedback enviado com sucesso!'})
    

class EmblemaListView(APIView):
    """
    View para listar os emblemas do usuário.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        aluno = get_object_or_404(Aluno, user__id=user_id)
        emblemas = Emblema.objects.filter(aluno=aluno)
        serializer = EmblemaSerializer(emblemas, many=True)
        return Response(serializer.data)


class PontuacaoListView(APIView):
    """
    View para listar as pontuações.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        if username:
            aluno = get_object_or_404(Aluno, user__username=username)
            pontuacao = get_object_or_404(Pontuacao, aluno=aluno)
            serializer = PontuacaoSerializer(pontuacao)
            return Response(serializer.data)
        
        pontuacoes = Pontuacao.objects.all().order_by('-pontos')
        serializer = PontuacaoSerializer(pontuacoes, many=True)
        return Response(serializer.data)

    
