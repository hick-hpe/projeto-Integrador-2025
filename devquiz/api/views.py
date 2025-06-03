from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Quiz, Questao, Certificado, Disciplina, Alternativa, RespostaAluno, Resposta, Desempenho
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, CertificadoPublicoSerializer, RespostaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

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
        request: {
            "alternativa_id": 1
        }
        """
        alternativa_id = request.data['alternativa_id']
        quiz = Quiz.objects.filter(id=quiz_id).first()
        questao = Questao.objects.filter(id=questao_id).first()
        alternativa = Alternativa.objects.filter(id=alternativa_id).first()
        
        resposta_aluno = RespostaAluno.objects.create(
            user=request.user,
            quiz=quiz,
            questao=questao,
            alternativa=alternativa
        )
        
        res_questao = Resposta.objects.filter(questao=questao).first()
        if res_questao and res_questao.alternativa == resposta_aluno.alternativa:
            desempenho = Desempenho.objects.filter(
                user=request.user,
                disciplina=quiz.disciplina,
                quiz=quiz
            ).first()
            
            desempenho.num_acertos += 1
            desempenho.save()


        serializer = RespostaSerializer(res_questao)
        return Response(serializer.data)
        
    questoes = Questao.objects.filter(quiz_id=quiz_id, id=questao_id)
    serializer = QuestaoSerializer(questoes, many=True)
    return Response(serializer.data)


@api_view(['GET'])  
@permission_classes([AllowAny])
def certificados(request, codigo):
    if codigo:
        try:
            certificado = Certificado.objects.get(codigo=codigo)
            serializer = CertificadoPublicoSerializer(certificado)
            return Response(serializer.data)
        except Certificado.DoesNotExist:
            return Response({'erro': 'Certificado não encontrado.'}, status=404)
    else:
        return Response({'erro': 'Código do certificado não fornecido.'}, status=400)


@api_view(['POST'])
def iniciar_quiz(request, quiz_id):
    """
    Constrói o objeto Desempenho, se ainda não existir.
    """
    quiz = Quiz.objects.filter(id=quiz_id).first()
    if not quiz:
        return Response({"error": "Quiz não encontrado"}, status=404)

    desempenho, created = Desempenho.objects.get_or_create(
        user=request.user,
        disciplina=quiz.disciplina,
        quiz=quiz,
        defaults={'num_acertos': 0}
    )

    return Response({"message": "Quiz Iniciado!!"})


@api_view(['POST'])
def desistir_quiz(request, quiz_id):
    """
    Excluir os objetos "RespostaAluno" e "Desempenho"
    """
    if quiz_id:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        desempenho = Desempenho.objects.filter(user=request.user, quiz=quiz).first()
        desempenho.delete()
        
        respostas = RespostaAluno.objects.filter(user=request.user, quiz=quiz)
        for r in respostas:
            r.delete()

        return Response({"message": "Quiz Desistido!!"})
    else:
        return Response({"error": "ID do quiz não enviado"})


@api_view(['POST'])
def concluir_quiz(request, quiz_id):
    """
    Concluir quize mostrar desempenho
    """
    if quiz_id:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        
        if quiz:
            desempenho = Desempenho.objects.filter(user=request.user, quiz=quiz).first()
            data = {
                "mensagem": "Quiz concluído com sucesso",
                "usuario": str(request.user),
                "quiz": quiz.nivel,
                "disciplina": quiz.disciplina.nome,
                "acertos": desempenho.num_acertos,
                "pontuacao": desempenho.num_acertos*10
            }
            respostas = RespostaAluno.objects.filter(user=request.user, quiz=quiz)
            for r in respostas:
                r.delete()

            return Response(data)
        else:
            return Response({"error": "Quiz não encontrado"})
    else:
        return Response({"error": "ID do quiz não enviado"})
