from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from certificado.views import gerar_certificado
from .models import models, Quiz, Questao, Disciplina, Alternativa, RespostaAluno, Resposta, Desempenho
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, RespostaSerializer, FeedbackSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import random
from django.core.mail import send_mail
from django.conf import settings

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def disciplinas_lista(request):
    if request.method == 'GET':
        disciplinas = Disciplina.objects.all()
        serializer = DisciplinaSerializer(disciplinas, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def disciplina_quizzes(request, disciplina_id):
    quizzes = Quiz.objects.filter(disciplina_id=disciplina_id)
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def quiz_questoes(request, quiz_id):
    """
    Veirficar se atingiu pelo 70% de acertos no nível anterior
    """
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
            return Response({'detail': 'Vc n pode fazer o nivel Intermediário!!'})
        
    elif quiz.nivel == "Avançado":
        desempenho = Desempenho.objects.filter(
            user=request.user,
            quiz__nivel="Intermediário",
            num_acertos__gte=7
        ).first()
        if not desempenho:
            return Response({'detail': 'Vc n pode fazer o nivel Avançado!!'})

    # else:
    print('------- entregando... ------')
    questoes = list(Questao.objects.filter(quiz_id=quiz_id))
    random.shuffle(questoes)
    questoes_aleatorias = questoes[:10]
    
    serializer = QuestaoSerializer(questoes_aleatorias, many=True)
    print('--- 0 -> ini')
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def questoes_detail(request, quiz_id, questao_id):
    if request.method == "POST":
        """
        request.data = {
            "alternativa_id": 1
        }
        """
        alternativa_id = request.data.get('alternativa_id')
        if not alternativa_id:
            return Response({'detail': 'alternativa_id não informado'}, status=status.HTTP_400_BAD_REQUEST)

        quiz = get_object_or_404(Quiz, id=quiz_id)
        questao = get_object_or_404(Questao, id=questao_id)
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)

        ultima_tentativa = RespostaAluno.objects.filter(user=request.user, quiz=quiz).aggregate(models.Max('tentativa'))['tentativa__max'] or 0
        nova_tentativa = ultima_tentativa + 1
        resposta_aluno, created = RespostaAluno.objects.get_or_create(
            user=request.user,
            quiz=quiz,
            questao=questao,
            tentativa=nova_tentativa,
            defaults={
                'alternativa': alternativa
            }
        )

        if not created:
            print('ja respondeu')
            return Response({'detail': 'Questão já respondida'}, status=status.HTTP_403_FORBIDDEN)

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
                user=request.user,
                disciplina=quiz.disciplina,
                quiz=quiz
            ).order_by('-id').first()

            if not desempenho:
                desempenho = Desempenho.objects.create(
                    user=request.user,
                    disciplina=quiz.disciplina,
                    quiz=quiz,
                    num_acertos=0
                )

            desempenho.num_acertos += 1
            desempenho.save()
            print(f"[DEBUG] {'Criado' if created else 'Atualizado'} desempenho: {desempenho.num_acertos}")
        else:
            print("[DEBUG] Alternativa incorreta.")

        return Response({
            'detail': 'Respondida!'
        })

    questao = get_object_or_404(Questao, quiz_id=quiz_id, id=questao_id)
    serializer = QuestaoSerializer(questao)
    return Response(serializer.data)


@api_view(['GET'])
# arrumar permissao pra nao permititr o aluno
def resposta_questao(request, quiz_id, questao_id):
    if quiz_id and questao_id:
        questao = get_object_or_404(Questao, quiz_id=quiz_id, id=questao_id)
        print('quiz.respostas')
        print(resposta := questao.resposta)
        serializer = RespostaSerializer(resposta)
        return Response({'detail': serializer.data})
    else:
        return Response({'detail': 'ID da questao e do quiz não fornecido!!'})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def iniciar_quiz(request, quiz_id):
    """
    Montar o objeto de controle para iniciar o quiz
    """

    if not quiz_id:
        return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    Desempenho.objects.create(
        user=request.user,
        quiz=quiz,
        disciplina=quiz.disciplina,
    )

    return Response({"detail": "Você iniciou o quiz!"})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def desistir_quiz(request, quiz_id):
    """
    Excluir os objetos "RespostaAluno" e "Desempenho" relacionados ao usuário e ao quiz.
    """
    if not quiz_id:
        return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    desempenho = Desempenho.objects.filter(
        user=request.user,
        quiz=quiz,
        disciplina=quiz.disciplina
    ).order_by('-id').first()
    desempenho.delete()

    respostas = RespostaAluno.objects.filter(user=request.user, quiz=quiz)
    respostas.delete()

    return Response({"detail": "Você desistiu do quiz!"})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def concluir_quiz(request, quiz_id):
    """
    Concluir quiz e mostrar desempenho
    """
    if not quiz_id:
        return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    desempenhos = Desempenho.objects.filter(
        user=request.user,
        quiz=quiz,
        disciplina=quiz.disciplina
    ).order_by('-id')
    
    desempenho = desempenhos.first()
    if not desempenho:
        return Response({"error": "Quiz não iniciado!"}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "usuario": str(request.user),
        "quiz": quiz.nivel,
        "disciplina": quiz.disciplina.nome,
        "acertos": desempenho.num_acertos,
    }

    if (desempenho.num_acertos / quiz.questoes.count()) >= 0.7:
        if quiz.nivel == "Avançado":
            gerar_certificado(data)

    # pq return isso ????
    return Response(data)


@api_view(['GET'])
def ultimos_desempenhos(request):
    """
    Retorna os 3 últimos desempenhos do usuário autenticado.
    """
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

@api_view(['POST'])
@permission_classes([AllowAny])
def feedbacks(request):
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