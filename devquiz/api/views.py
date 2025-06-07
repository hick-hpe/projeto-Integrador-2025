from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import models, Quiz, Questao, Disciplina, Alternativa, RespostaAluno, Resposta, Desempenho
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, RespostaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import random

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
    questoes = list(Questao.objects.filter(quiz_id=quiz_id))
    random.shuffle(questoes)
    questoes_aleatorias = questoes[:10]
    
    serializer = QuestaoSerializer(questoes_aleatorias, many=True)
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

        if correto:
            desempenho = Desempenho.objects.filter(
                user=request.user,
                disciplina=quiz.disciplina,
                quiz=quiz,
            ).order_by('-id').first()
            desempenho.num_acertos += 1
            desempenho.save()

        # serializer = RespostaSerializer(res_questao)
        return Response({
            # 'correto': correto, **serializer.data
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


# @permission_classes([IsAuthenticated])
# @api_view(['POST', 'PUT', 'DELETE'])
# def crud_quiz(request, quiz_id=None):
#     disciplina = request.data.get('disciplina_id')
#     nivel = request.data.get('nivel')
#     descricao = request.data.get('descricao')
#     alternativas = []
#     # for a in request.data.get('alternativas'):
#         # alternativas.append(a)

#     if not all([disciplina, descricao, nivel]):
#         return Response({'error': 'Campos obrigatórios não enviados.'}, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == "POST":
#         quiz = Quiz.objects.create(disciplina, nivel, descricao)
#         return Response({'detail': 'Quiz criado com sucesso!'})

#     elif request.method == "PUT":
#         quiz = get_object_or_404(Quiz, id=quiz_id)

#         if quiz:
#             Quiz.objects.update_or_create(
#                 id=quiz_id,
#                 disciplina=disciplina,
#                 defaults={
#                     'descricao': descricao
#                 }
#             )

#             return Response({'detail': 'Quiz atualizado com sucesso!'})
#         else:
#             return Response({'error': 'Quiz não encontrado!'})
        
    
#     elif request.method == 'DELETE':
#         quiz = get_object_or_404(Quiz, id=quiz_id)

#         if quiz:
#             quiz.delete()
#             return Response({'detail': 'Quiz excluído com sucesso!'})
#         else:
#             return Response({'error': 'Quiz não encontrado!'})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def iniciar_quiz(request, quiz_id):
    """
    Montar o objeto de controle para iniciar o quiz
    """
    # Desempenho.objects.all().delete() # remover depois ;-;
    # RespostaAluno.objects.all().delete() # remover depois ;-;
    
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
        print("not quiz -------")
        return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)
    print("obteve quiz -------")

    desempenhos = Desempenho.objects.filter(
        user=request.user,
        quiz=quiz,
        disciplina=quiz.disciplina
    ).order_by('-id')
    
    if desempenhos.count() > 3:
        for d in desempenhos[3:]:
            d.delete()

    desempenho = desempenhos.first()
    if not desempenho:
        print("desempenho -------")
        return Response({"error": "Quiz não iniciado!"}, status=status.HTTP_404_NOT_FOUND)

    print("desempenho -------")

    data = {
        "mensagem": "Quiz concluído com sucesso!",
        "usuario": str(request.user),
        "quiz": quiz.nivel,
        "disciplina": quiz.disciplina.nome,
        "acertos": desempenho.num_acertos,
        "total_questoes": quiz.questoes.count(),
        "pontuacao": desempenho.num_acertos * 10
    }

    RespostaAluno.objects.filter(user=request.user, quiz=quiz).delete()

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
    