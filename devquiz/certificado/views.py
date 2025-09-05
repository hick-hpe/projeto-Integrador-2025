from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from api.models import Aluno, Certificado, Disciplina
from api.serializers import CertificadoSerializer
import pdfkit
import os
import base64
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, JsonResponse
import random
from django.templatetags.static import static

class CertificadoDetailView(APIView):
    """
    View para obter detalhes de um certificado específico.
    """
    permission_classes = [AllowAny]

    def get(self, request, codigo):
        if codigo:
            try:
                certificado = Certificado.objects.get(codigo=codigo)
                serializer = CertificadoSerializer(certificado)
                return Response(serializer.data)
            except Certificado.DoesNotExist:
                return Response({'erro': 'Certificado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'erro': 'Código do certificado não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)


def converter_imagem_para_base64(caminho):
    """
    Converte uma imagem em um caminho para uma string base64.
    """
    with open(caminho, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


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


def gerar_certificado(data):
    """
    Gerar apenas se o aluno obteve pelo menos 70% de acertos
    """
    aluno = get_object_or_404(Aluno, user__username=data['aluno'])
    disciplina = get_object_or_404(Disciplina, nome=data['disciplina'])

    Certificado.objects.get_or_create(
        aluno=aluno,
        disciplina=disciplina,
        percentual_acertos=data['acertos'],
        defaults={
            'codigo': gerar_codigo_certificado()
        }
    )


class CertificadoPDFView(APIView):
    """
    View para exibir a lista de certificados.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        certificados = list(Certificado.objects.all().values())
        return JsonResponse({
            'certificados': certificados
        })


class CertificadoDownloadView(APIView):
    """
    View para gerar e baixar o certificado em PDF.
    """
    permission_classes = [AllowAny]
    
    def get(self, request, codigo):
        if codigo:
            try:
                disciplina = Disciplina.objects.get(pk=1)
                
                certificado = get_object_or_404(Certificado, codigo=codigo, aluno=request.user.aluno, disciplina=disciplina)
                nome = request.user.username
                percentual_acertos = certificado.percentual_acertos

                data_formatada = converter_data_para_extenso(datetime.today())
                logo_path = os.path.join('static', 'img', 'logo.png')
                
                logo_base64 = converter_imagem_para_base64(logo_path)
                css_url = request.build_absolute_uri(static('css/certificado_pdf.css'))

                contexto = {
                    "nome": nome.upper(),
                    "data": data_formatada,
                    "logo_base64": logo_base64,
                    "percentual_acertos": percentual_acertos,
                    'css_url': css_url
                }

                rendered = render(request, 'certificado_pdf.html', contexto).content.decode('utf-8')
                pdf_path = f'certificado_{nome.replace(" ", "_")}.pdf'
                pdfkit.from_string(rendered, pdf_path, options={'enable-local-file-access': ''})
                
                return FileResponse(open(pdf_path, 'rb'), as_attachment=True)
            
            except Certificado.DoesNotExist:
                return Response({'erro': 'Certificado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'erro': 'Código do certificado não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

