from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Quiz, Questao, Certificado, Disciplina, Alternativa, RespostaAluno, Resposta, Desempenho
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, CertificadoPublicoSerializer
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
            "questao_id": 1,
            "alternativa_id": 1
        }
        """
        alternativa_id = request.data['alternativa_id']
        quiz = Quiz.objects.filter(id=quiz_id).first(),
        questao = Questao.objects.filter(id=questao_id).first(),
        alternativa = Alternativa.objects.filter(id=alternativa_id).first(),
        
        resposta_aluno = RespostaAluno.objects.create(
            user=request.user,
            quiz=quiz,
            questao=questao,
            alternativa=alternativa
        )
        
        res_gabarito = Resposta(questao=questao)
        if res_gabarito.alternativa == resposta_aluno.alternativa:
            desempenho = Desempenho.objects.filter(
                user=request.user,
                disciplina=quiz.disciplina,
                quiz=quiz,
            )
            
            desempenho.num_acertos += 1
            desempenho.save()
        
        
        return Response({"message": f"Enviando repsosta da questão {questao_id}!!"})

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
    Contruir objetos "Desempenho", depois recuperá-los em "concluir_quiz()"
    """
    quiz = Quiz.objects.filter(id=quiz_id)
    desempenho = Desempenho.objects.filter(
        user=request.user,
        disciplina=quiz.disciplina,
        quiz=quiz
    )
    
    if not desempenho:
        desempenho = Desempenho.objects.create(
            user=request.user,
            disciplina=quiz.disciplina,
            quiz=quiz
        )
    
    if quiz_id:
        return Response({"message": "Quiz Iniciado!!"})
    else:
        return Response({"error": "ID do quiz não enviado"})


@api_view(['POST'])
def desistir_quiz(request, quiz_id):
    """
    Excluir os objetos "RespostaAluno"
    """
    if quiz_id:
        return Response({"message": "Quiz Desistido!!"})
    else:
        return Response({"error": "ID do quiz não enviado"})


@api_view(['POST'])
def concluir_quiz(request, quiz_id):
    """
    Continuar, recuperar os objetos "RespostaAluno"
    """
    if quiz_id:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if quiz:
            pontuacao = 0
            acertos = 0
            respostas = request.data.get('respostas', [])

            for r in respostas:
                questao = Questao.objects.get(id=r['questao_id'], quiz=quiz)
                alternativa = Alternativa.objects.get(id=r['alternativa_id'], questao=questao)

                if alternativa.correta:
                    acertos += 1
                    pontuacao += 10

            data = {
                "mensagem": "Quiz concluído com sucesso",
                "usuario": str(request.user),
                "quiz": quiz.nivel,
                "disciplina": quiz.disciplina.nome,
                "acertos": acertos,
                "pontuacao": pontuacao
            }
            return Response(data)
        else:
            return Response({"error": "Quiz não encontrado"})
    else:
        return Response({"error": "ID do quiz não enviado"})
