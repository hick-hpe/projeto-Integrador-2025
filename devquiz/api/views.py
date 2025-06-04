from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Quiz, Questao, Disciplina, Alternativa, RespostaAluno, Resposta, Desempenho
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, CertificadoPublicoSerializer, RespostaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
    questoes = Questao.objects.filter(quiz_id=quiz_id)
    serializer = QuestaoSerializer(questoes, many=True)
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
            return Response({'detail': 'alternativa_id não informado'}, status=400)

        quiz = get_object_or_404(Quiz, id=quiz_id)
        questao = get_object_or_404(Questao, id=questao_id)
        alternativa = get_object_or_404(Alternativa, id=alternativa_id)

        resposta_aluno, created = RespostaAluno.objects.get_or_create(
            user=request.user,
            quiz=quiz,
            questao=questao,
            defaults={'alternativa': alternativa}
        )

        if not created:
            return Response({'detail': 'Questão já respondida'}, status=status.HTTP_403_FORBIDDEN)

        resposta_aluno.alternativa = alternativa
        resposta_aluno.save()

        res_questao = get_object_or_404(Resposta, questao=questao)
        correto = res_questao.alternativa == alternativa

        if correto:
            desempenho, _ = Desempenho.objects.get_or_create(
                user=request.user,
                disciplina=quiz.disciplina,
                quiz=quiz,
                defaults={'num_acertos': 0}
            )
            desempenho.num_acertos += 1
            desempenho.save()

        serializer = RespostaSerializer(res_questao)
        return Response({
            'correto': correto, **serializer.data
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
def desistir_quiz(request, quiz_id):
    """
    Excluir os objetos "RespostaAluno" e "Desempenho" relacionados ao usuário e ao quiz.
    """
    if not quiz_id:
        return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    desempenho = Desempenho.objects.filter(user=request.user, quiz=quiz).first()
    if desempenho:
        desempenho.delete()

    respostas = RespostaAluno.objects.filter(user=request.user, quiz=quiz)
    respostas.delete()

    return Response({"message": "Quiz desistido com sucesso!"})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def concluir_quiz(request, quiz_id):
    """
    Concluir quiz e mostrar desempenho
    """
    if not quiz_id:
        return Response({"error": "ID do quiz não enviado"}, status=status.HTTP_400_BAD_REQUEST)

    quiz = get_object_or_404(Quiz, id=quiz_id)

    desempenho = Desempenho.objects.filter(user=request.user, quiz=quiz).first()
    if not desempenho:
        return Response({"error": "Desempenho não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "mensagem": "Quiz concluído com sucesso!",
        "usuario": str(request.user),
        "quiz": quiz.nivel,
        "disciplina": quiz.disciplina.nome,
        "acertos": desempenho.num_acertos,
        "pontuacao": desempenho.num_acertos * 10
    }

    RespostaAluno.objects.filter(user=request.user, quiz=quiz).delete()

    return Response(data)
