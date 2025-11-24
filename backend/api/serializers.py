from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    CustomUser, Disciplina, Pontuacao, Quiz, Questao,
    Alternativa, Resposta, RespostaAluno,
    Feedback, Certificado, EmblemaUser
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id', 'nome']


class QuizSerializer(serializers.ModelSerializer):
    disciplina = serializers.SlugRelatedField(
        slug_field="nome",
        queryset=Disciplina.objects.all()
    )
    
    disciplina_id = serializers.PrimaryKeyRelatedField(
        source='disciplina',
        queryset=Disciplina.objects.all(),
        write_only=True
    )

    questoes = serializers.SerializerMethodField()

    def get_questoes(self, obj):
        return QuestaoSerializer(obj.questoes.all(), many=True).data

    class Meta:
        model = Quiz
        fields = ['id', 'disciplina', 'disciplina_id', 'nivel', 'descricao', 'questoes']
    

class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = ['id', 'texto']


class QuestaoSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all(),
        write_only=True
    )
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
    aluno = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    questao = serializers.PrimaryKeyRelatedField(queryset=Questao.objects.all())
    alternativa = serializers.PrimaryKeyRelatedField(queryset=Alternativa.objects.all())

    class Meta:
        model = RespostaAluno
        fields = ['id', 'aluno', 'questao', 'alternativa']


class CertificadoSerializer(serializers.ModelSerializer):
    aluno = serializers.CharField(source='aluno.user.username')
    disciplina = serializers.CharField(source='disciplina.nome')
    data_emissao = serializers.DateField(format="%d/%m/%Y", read_only=True)

    class Meta:
        model = Certificado
        fields = ['codigo', 'aluno', 'disciplina', 'data_emissao']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['email', 'assunto', 'mensagem']


class EmblemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmblemaUser
        fields = ['nome', 'descricao', 'logo']


class EmblemaUserSerializer(serializers.ModelSerializer):
    aluno = serializers.SerializerMethodField()

    class Meta:
        model = EmblemaUser
        fields = ['aluno', 'nome', 'descricao', 'logo']

    def get_aluno(self, obj):
        return obj.aluno.user.username


class PontuacaoSerializer(serializers.ModelSerializer):
    aluno = serializers.SerializerMethodField()

    class Meta:
        model = Pontuacao
        fields = ['aluno', 'pontos']

    def get_aluno(self, obj):
        return obj.aluno.user.username


#Json serializer de cadastro
# Utilizando os módulos importados no início do documento
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data.get("username") or validated_data["email"],
            email = validated_data["email"],
            password = validated_data["password"],
            first_name = validated_data.get("first_name", ""),
            last_name = validated_data.get("last_name", "")
        )
        return user
