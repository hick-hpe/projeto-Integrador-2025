from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Quiz, Questao, Certificado
from .serializers import DisciplinaSerializer, QuizSerializer, QuestaoSerializer, CertificadoPublicoSerializer


@api_view(['GET', 'POST'])
def disciplinas_lista(request):
    if request.method == 'GET':
        disciplinas = Disciplina.objects.all()
        serializer = DisciplinaSerializer(disciplinas, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def disciplina_quizzes(request, disciplina_id):
    if request.method == 'GET':
        quizzes = Quiz.objects.filter(disciplina_id=disciplina_id)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    return Response({"msg": "GET"})


@api_view(['GET'])
def quiz_questoes(request, quiz_id, questao_id=None):
    if questao_id:
        questoes = Questao.objects.filter(quiz_id=quiz_id, id=questao_id)
    else:
        questoes = Questao.objects.filter(quiz_id=quiz_id)
    
    serializer = QuestaoSerializer(questoes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def questao_resposta(request, quiz_id, questao_id):
    try:
        questao = Questao.objects.get(quiz_id=quiz_id, id=questao_id)
        alternativa = questao.alternativas.filter(correta=True).first()
        data = {
            'questao': questao.descricao,
            'alternativa_correta': alternativa.texto,
            'explicacao': questao.explicacao
        }
        return Response(data)
    except Questao.DoesNotExist:
        return Response({'erro': 'Questão não encontrada.'}, status=404)


@api_view(['GET'])
def certificados(request, codigo=None):
    if codigo:
        try:
            certificado = Certificado.objects.get(codigo=codigo)
            serializer = CertificadoPublicoSerializer(certificado)
            return Response(serializer.data)
        except Certificado.DoesNotExist:
            return Response({'erro': 'Certificado não encontrado.'}, status=404)
