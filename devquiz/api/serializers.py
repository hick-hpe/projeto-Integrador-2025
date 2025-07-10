from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Aluno, Disciplina, Quiz, Questao,
    Alternativa, Resposta, RespostaAluno,
    Feedback,
    Certificado
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AlunoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Aluno
        fields = ['id', 'user', 'foto_perfil']


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id', 'nome']


class QuizSerializer(serializers.ModelSerializer):
    disciplina = serializers.CharField(source="disciplina.nome")
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(), source='disciplina', write_only=True
    )

    class Meta:
        model = Quiz
        fields = ['id', 'disciplina', 'disciplina_id', 'nivel', 'descricao']


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = ['id', 'texto']


class QuestaoSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    alternativas = AlternativaSerializer(many=True, read_only=True)

    class Meta:
        model = Questao
        fields = ['id', 'quiz', 'descricao', 'alternativas']


class RespostaSerializer(serializers.ModelSerializer):
    questao_id = serializers.PrimaryKeyRelatedField(queryset=Questao.objects.all(), write_only=True)
    alternativa_id = serializers.PrimaryKeyRelatedField(queryset=Alternativa.objects.all(), write_only=True)
    questao = serializers.SerializerMethodField(read_only=True)
    alternativa = serializers.SerializerMethodField(read_only=True)

    def get_questao(self, obj):
        return obj.questao.descricao
    
    def get_alternativa(self, obj):
        return obj.alternativa.texto

    class Meta:
        model = Resposta
        fields = ['id', 'questao_id', 'questao', 'alternativa', 'alternativa_id', 'explicacao']
        read_only_fields = ['questao', 'alternativa', 'explicacao']


class RespostaAlunoSerializer(serializers.ModelSerializer):
    aluno = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all())
    questao = serializers.PrimaryKeyRelatedField(queryset=Questao.objects.all())
    alternativa = serializers.PrimaryKeyRelatedField(queryset=Alternativa.objects.all())

    class Meta:
        model = RespostaAluno
        fields = ['id', 'aluno', 'questao', 'alternativa']


# class PontuacaoSerializer(serializers.ModelSerializer):
#     usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())

#     class Meta:
#         model = Pontuacao
#         fields = ['id', 'usuario', 'quiz', 'pontuacao']


class CertificadoSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='usuario.username')
    disciplina = serializers.CharField(source='disciplina.nome')
    data_emissao = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Certificado
        fields = ['codigo', 'usuario', 'disciplina', 'data_emissao']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['email', 'assunto', 'mensagem']