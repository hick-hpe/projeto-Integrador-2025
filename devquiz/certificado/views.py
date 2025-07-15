from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from api.models import Certificado, Disciplina
from api.serializers import CertificadoSerializer
import pdfkit
import os
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import FileResponse
import random


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
    codigo += "".join(random.choices(alfabeto, k=5)) + random.randint(11111, 99999)
    return codigo


def gerar_certificado(data):
    """
    Gerar apenas se o aluno obteve pelo menos 70% de acertos
    """
    Certificado.objects.get_or_create(
        codigo=gerar_codigo_certificado(),
        usuario=data['user'],
        quiz=data['quiz'],
        disciplina=data['disciplina'],
        acertos=data['acertos']
    )


class CertificadoPDFView(APIView):
    """
    View para renderizar o certificado em PDF.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'certificado_pdf.html')


class CertificadoDownloadView(APIView):
    """
    View para gerar e baixar o certificado em PDF.
    """
    permission_classes = [AllowAny]
    
    def get(self, request, codigo):
        if codigo:
            try:
                print('> disciplina ------------')
                disciplina = Disciplina.objects.get(pk=1)
                
                print('> certificado ------------')
                certificado = Certificado.objects.get(
                    usuario=request.user,
                    disciplina=disciplina
                )
                nome = request.user.username
                percentual_acertos = certificado.percentual_acertos

                print('> formatar data ------------')
                data_formatada = converter_data_para_extenso(datetime.today())
                logo_path = os.path.join('static', 'img', 'logo.png')
                
                print('> logo_path ------------')
                print(logo_path)
                logo_base64 = converter_imagem_para_base64(logo_path)
                print('> logo_path OK ---------')

                print('> criar contexto ------------')
                contexto = {
                    "nome": nome.upper(),
                    "data": data_formatada,
                    "logo_base64": logo_base64,
                    "percentual_acertos": percentual_acertos
                }
                print(contexto)
                print('> criar contexto OK ---------')

                print('> renderizar ------------')
                rendered = render(request, 'certificado_pdf.html', contexto).content.decode('utf-8')
                pdf_path = f'certificado_{nome.replace(" ", "_")}.pdf'
                pdfkit.from_string(rendered, pdf_path, options={'enable-local-file-access': ''})
                print('> renderizar OK ---------')

                
                print('> retornar ao frontend ------------')
                return FileResponse(open(pdf_path, 'rb'), as_attachment=True)
            
            except Certificado.DoesNotExist:
                return Response({'erro': 'Certificado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'erro': 'Código do certificado não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)
