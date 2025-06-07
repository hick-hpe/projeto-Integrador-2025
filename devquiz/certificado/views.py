from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from api.models import Certificado, Disciplina # teste
from api.serializers import CertificadoSerializer
# import pdfkit
import os
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import FileResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def certificados(request, codigo):
    if codigo:
        try:
            certificado = Certificado.objects.get(codigo=codigo)
            serializer = CertificadoSerializer(certificado)
            return Response(serializer.data)
        except Certificado.DoesNotExist:
            return Response({'erro': 'Certificado não encontrado.'}, status=404)
    return Response({'erro': 'Código do certificado não fornecido.'}, status=400)


def imagem_para_base64(caminho):
    with open(caminho, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def data_extenso(data: datetime):
    meses = [
        "janeiro", "fevereiro", "março", "abril",
        "maio", "junho", "julho", "agosto",
        "setembro", "outubro", "novembro", "dezembro"
    ]
    return f"{data.day} de {meses[data.month - 1]} de {data.year}"


@api_view(['POST'])
def gerar_certificado(request):
    """
    Gerar apenas se o aluno obteve pelo menos 70% de acertos
    """
    pass

def certificado(request):
    return render(request, 'certificado_pdf.html')

# @api_view(['GET'])
# @permission_classes([AllowAny]) # erro: rever as permissões ;-;
# def certificado_download(request, codigo=None):
#     # if codigo:
#         print('sera???')
#         try:
#             print('> disciplina ------------')
#             disciplina = Disciplina.objects.get(pk=1) # teste
#             # disciplina.logo
            
#             print('> certificado ------------')
#             certificado = Certificado.objects.get(
#                 usuario=request.user,
#                 disciplina=disciplina # teste
#             )
#             nome = request.user.username
#             percentual_acertos = certificado.percentual_acertos

#             print('> formatar data ------------')
#             data_formatada = data_extenso(datetime.today())
#             logo_path = os.path.join('static', 'img', 'logo.png')
            
#             print('> logo_path ------------')
#             print(logo_path)
#             logo_base64 = imagem_para_base64(logo_path)
#             print('> logo_path OK ---------')

#             print('> criar contexto ------------')
#             contexto = {
#                 "nome": nome.upper(),
#                 "data": data_formatada,
#                 "logo_base64": logo_base64,
#                 "percentual_acertos": percentual_acertos
#             }
#             print(contexto)
#             print('> criar contexto OK ---------')

#             print('> renderizar ------------')
#             rendered = render(request, 'certificado_pdf.html', contexto).content.decode('utf-8')
#             pdf_path = f'certificado_{nome.replace(" ", "_")}.pdf'
#             pdfkit.from_string(rendered, pdf_path, options={'enable-local-file-access': ''})
#             print('> renderizar OK ---------')

            
#             print('> retornar ao frontend ------------')
#             # return Response({'detail':'certificado'})
#             return FileResponse(open(pdf_path, 'rb'), as_attachment=True)
        
#         except Certificado.DoesNotExist:
#             return Response({'erro': 'Certificado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    # return Response({'erro': 'Código do certificado não fornecido.'}, status=400)
