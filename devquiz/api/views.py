from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


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
    return Response({"msg": "Questões do Quiz"})


@api_view(['GET'])
def questao_resposta(request, quiz_id, questao_id):
    return Response({"msg": "Resposta e explicação da questão"})


@api_view(['GET'])
def certificados(request, codigo):
    return Response({"msg": "Certificado do aluno!!!"})