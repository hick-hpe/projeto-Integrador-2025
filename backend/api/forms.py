from django import forms
from .models import CustomUser, Codigo, Disciplina, Quiz, Questao, Alternativa, RespostaAluno, Feedback, Emblema

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'foto_perfil', 'password')

class CodigoForm(forms.ModelForm):
    class Meta:
        model = Codigo
        fields = ('codigo')

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ('nome')

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('disciplina', 'nivel', 'descricao')

class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = ('quiz', 'descricao')

class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ('questao', 'texto')

class RespostaAlunoForm(forms.ModelForm):
    class Meta:
        model = RespostaAluno
        fields = ('quiz', 'questao', 'alternativa')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('assunto', 'mensagem', 'email')

class EmblemaForm(forms.ModelForm):
    class Meta:
        model = Emblema
        fields = ('aluno', 'nome', 'descricao', 'logo')
