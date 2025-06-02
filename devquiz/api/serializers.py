from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Aluno, Disciplina, Quiz, Questao,
    Alternativa, Resposta, RespostaAluno,
    # Pontuacao,
    Certificado
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


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
    disciplina = DisciplinaSerializer(read_only=True)
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(), source='disciplina', write_only=True
    )

    class Meta:
        model = Quiz
        fields = ['id', 'disciplina', 'disciplina_id', 'nivel', 'descricao']


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = ['id', 'texto', 'correta']


class QuestaoSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    alternativas = AlternativaSerializer(many=True, read_only=True)

    class Meta:
        model = Questao
        fields = ['id', 'quiz', 'descricao', 'alternativas']


class RespostaSerializer(serializers.ModelSerializer):
    questao = serializers.PrimaryKeyRelatedField(queryset=Questao.objects.all())
    alternativa = serializers.PrimaryKeyRelatedField(queryset=Alternativa.objects.all())

    class Meta:
        model = Resposta
        fields = ['id', 'questao', 'alternativa', 'explicacao']


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
    usuario = UserSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='usuario', write_only=True
    )
    disciplina = DisciplinaSerializer(read_only=True)
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(), source='disciplina', write_only=True
    )

    class Meta:
        model = Certificado
        fields = ['id', 'codigo', 'usuario', 'usuario_id', 'disciplina', 'disciplina_id', 'data_emissao']

class CertificadoPublicoSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    disciplina = serializers.CharField(source='disciplina.nome')

    class Meta:
        model = Certificado
        fields = ['codigo', 'usuario', 'disciplina', 'data_emissao']

    def get_usuario(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data