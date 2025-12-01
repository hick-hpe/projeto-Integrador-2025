from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Disciplina, Quiz, Questao,
    Alternativa, RespostaQuestao, RespostaAluno,
    Certificado, Emblema, EmblemaUser, Tentativa
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
        fields = ['id', 'titulo', 'disciplina', 'tipo_questoes', 'disciplina_id', 'nivel', 'descricao', 'questoes']


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = ['id', 'texto']


class QuestaoRespostaSerializer(serializers.ModelSerializer):
    alternativas = AlternativaSerializer(many=True)
    resposta_correta = serializers.SerializerMethodField()
    explicacao = serializers.SerializerMethodField()

    class Meta:
        model = Questao
        fields = ['id', 'descricao', 'alternativas', 'resposta_correta', 'explicacao']

    def get_resposta_correta(self, obj):
        # obj.resposta é o related_name do seu OneToOneField
        if hasattr(obj, 'resposta'):
            return obj.resposta.alternativa.id
        return None

    def get_explicacao(self, obj):
        if hasattr(obj, 'resposta'):
            return obj.resposta.explicacao
        return None
        

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
        model = RespostaQuestao
        fields = ['id', 'questao_id', 'questao', 'alternativa', 'alternativa_id', 'explicacao']
        read_only_fields = ['questao', 'alternativa', 'explicacao']


class RespostaAlunoSerializer(serializers.ModelSerializer):
    aluno = serializers.PrimaryKeyRelatedField(read_only=True)
    questao = serializers.PrimaryKeyRelatedField(read_only=True)
    alternativa = serializers.PrimaryKeyRelatedField(read_only=True)

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
        

class EmblemaSerializer(serializers.ModelSerializer):
    disciplina = serializers.SerializerMethodField()

    def get_disciplina(self, obj):
        return obj.disciplina.nome

    class Meta:
        model = Emblema
        fields = ['id', 'nome', 'descricao', 'logo', 'disciplina']


class EmblemaUserSerializer(serializers.ModelSerializer):
    emblema = EmblemaSerializer()

    class Meta:
        model = EmblemaUser
        fields = ['id', 'emblema', 'conquistado_em']


class TentativaSerializer(serializers.ModelSerializer):
    disciplina = serializers.SerializerMethodField()
    nivel = serializers.SerializerMethodField()
    quiz_id = serializers.SerializerMethodField()

    def get_disciplina(self, obj):
        return obj.quiz.disciplina.nome

    def get_nivel(self, obj):
        return obj.quiz.nivel
    
    def get_quiz_id(self, obj):
        return obj.quiz.id
    
    class Meta:
        model = Tentativa
        fields = ['id', 'nivel', 'aprovado', 'disciplina', 'quiz_id', 'status_quiz']
    
