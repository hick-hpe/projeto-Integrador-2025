from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from api.models import CustomUser, Certificado, Disciplina
from api.serializers import CertificadoSerializer
import io
import pdfkit
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
import random

class ValidarCertificadoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("\n===================== [VALIDAÇÃO DE CERTIFICADO] =====================")

        codigo = request.data.get('codigo')
        matricula = request.data.get('matricula')

        print(f"[INPUT] Código: {codigo}")
        print(f"[INPUT] Matrícula: {matricula}")

        # Falta de dados → valido = False
        if not codigo or not matricula:
            print("[ERRO] Código ou matrícula não informados.")
            return Response({"valido": False}, status=status.HTTP_200_OK)

        # Verifica aluno
        try:
            aluno_temp = CustomUser.objects.get(matricula=matricula)
        except CustomUser.DoesNotExist:
            print("[ERRO] Aluno não encontrado.")
            return Response({"valido": False}, status=status.HTTP_200_OK)

        # Verifica certificado
        try:
            certificado = Certificado.objects.get(codigo=codigo, aluno=aluno_temp)
        except Certificado.DoesNotExist:
            print("[ERRO] Certificado não encontrado ou não pertence a este aluno.")
            return Response({"valido": False}, status=status.HTTP_200_OK)

        # Certificado válido
        print("[SUCESSO] Certificado válido.")
        return Response({"valido": True}, status=status.HTTP_200_OK)


def converter_data_para_extenso(data: datetime):
    """
    Converte uma data para o formato "dia de mês de ano".
    """
    meses = [
        "janeiro", "fevereiro", "março", "abril",
        "maio", "junho", "julho", "agosto",
        "setembro", "outubro", "novembro", "dezembro"
    ]
    return f"{data.day} de {meses[data.month - 1]} de {data.year}"


def gerar_codigo_certificado():
    """
    Gera um código único para o certificado.
    """
    codigo = ""
    alfabeto = [chr(i) for i in range(65, 91)]
    random.shuffle(alfabeto)
    codigo += "".join(random.choices(alfabeto, k=5)) + str(random.randint(11111, 99999))
    return codigo


def gerar_certificado_no_banco(data):
    """
    Gerar apenas se o aluno obteve pelo menos 70% de acertos
    """
    aluno = get_object_or_404(CustomUser, user__username=data['aluno'])
    disciplina = get_object_or_404(Disciplina, nome=data['disciplina'])

    Certificado.objects.get_or_create(
        aluno=aluno,
        disciplina=disciplina,
        defaults={
            'codigo': gerar_codigo_certificado()
        }
    )

# rever privilégio -> testes
class CertificadoListView(APIView):
    """
    View para exibir a lista de certificados.
    """
    permission_classes = [AllowAny] # admin?

    def get(self, request):
        aluno = get_object_or_404(CustomUser, user=request.user)
        certificados = Certificado.objects.filter(aluno=aluno)
        serializer = CertificadoSerializer(certificados, many=True)
        return Response(serializer.data)


def baixar_certificado(request, certificado, aluno):
    nome = aluno.user.username
    data_formatada = converter_data_para_extenso(datetime.today())

    contexto = {
        "nome": nome.upper(),
        "disciplina": certificado.disciplina.nome,
        "data": data_formatada,
    }

    rendered = render(request, 'certificado_pdf.html', contexto).content.decode('utf-8')

    # gera PDF em memoria
    pdf_bytes = io.BytesIO()
    pdfkit.from_string(rendered, pdf_bytes, options={'enable-local-file-access': ''})
    pdf_bytes.seek(0) # move cursor de leitura para o inicio do arquivo (pra onde ele vai começar a ler pro response)

    filename = f'certificado_{nome.replace(" ", "_")}.pdf'
    # as_attachment=True -> força o navegador a baixar o arquivo em vez de abrir na tela.
    # filename=filename -> define o nome do arquivo que o usuário vai receber.
    return FileResponse(pdf_bytes, as_attachment=True, filename=filename)


class CertificadoDownloadView(APIView):
    """
    View para gerar e baixar o certificado em PDF.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, codigo):
        if not codigo:
            return Response({'erro': 'Código do certificado não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Busca o certificado pelo código
        certificado = get_object_or_404(Certificado, codigo=codigo)
        aluno = certificado.aluno  # pega o aluno relacionado ao certificado
        
        return baixar_certificado(request, certificado, aluno)
