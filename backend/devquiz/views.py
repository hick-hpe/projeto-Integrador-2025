from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    return JsonResponse({'message': 'API ON!!!'})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Quiz, Question
from .serializers import QuizSerializer

class QuizSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        disciplina = request.data.get("disciplina")
        nivel = request.data.get("nivel")
        qs = Quiz.objects.all()
        if disciplina:
            qs = qs.filter(disciplina__icontains=disciplina)
        if nivel:
            qs = qs.filter(nivel__iexact=nivel)
        serializer = QuizSerializer(qs, many=True)
        return Response({"quizzes": serializer.data})

class QuizDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({"error":"Quiz não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        quiz_id = request.data.get("quiz_id")
        question_id = request.data.get("question_id")
        answer = request.data.get("answer")
        try:
            q = Question.objects.get(pk=question_id, quiz_id=quiz_id)
        except Question.DoesNotExist:
            return Response({"error":"Questão não encontrada"}, status=status.HTTP_400_BAD_REQUEST)
        correto = (answer == q.correct_choice)
        feedback = "Correto!" if correto else f"Errado. Resposta certa: {q.correct_choice}"
        return Response({"correto": correto, "feedback": feedback})
    