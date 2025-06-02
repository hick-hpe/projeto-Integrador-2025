from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Quiz, Questao, Certificado, Disciplina, Alternativa, Aluno
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
    if request.method == 'GET':
        quizzes = Quiz.objects.filter(disciplina_id=disciplina_id)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    return Response({"msg": "GET"})


@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def quiz_questoes(request, quiz_id, questao_id=None):
    if request.method == "POST":
        # Buscar a questão
        questao = Questao.objects.get(quiz_id=quiz_id, id=questao_id)
        alternativa = Alternativa.objects.get(
            questao=questao, id=request.data.get('alternativa_id')
        )
        
        # Comparar com a resposta certa
        if alternativa.correta:
            return Response({"msg": "POST - Resposta correta", "explicacao": questao.explicacao})
        else:
            return Response({"msg": "POST - Resposta incorreta", "explicacao": questao.explicacao})
    

    if questao_id:
        questoes = Questao.objects.filter(quiz_id=quiz_id, id=questao_id)
    else:
        questoes = Questao.objects.filter(quiz_id=quiz_id)
    
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
def desistir_quiz(request, quiz_id):
    if quiz_id:
        return Response({"message": "Quiz Desistido!!"})
    else:
        return Response({"error": "ID do quiz não enviado"})


@api_view(['POST'])
def concluir_quiz(request, quiz_id):
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
