from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from api.models import CustomUser, Certificado, Disciplina
from api.serializers import CertificadoSerializer
import pdfkit
import os
import base64
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, JsonResponse
import random
from django.templatetags.static import static

class ValidarCertificadoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("\n===================== [VALIDAÇÃO DE CERTIFICADO] =====================")

        codigo = request.data.get('codigo')
        matricula = request.data.get('matricula')

        print(f"[INPUT] Código: {codigo}")
        print(f"[INPUT] Matrícula: {matricula}")

        if not codigo or not matricula:
            print("[ERRO] Código ou matrícula não informados.")
            return Response(
                {'erro': 'É necessário informar o código do certificado e a matrícula do aluno.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # teste
        # return Response({"detail": "válido!!!"}) 

        try:
            print("[BUSCA] Verificando aluno e disciplina...")
            disciplina = Disciplina.objects.get(pk=1)
            aluno = CustomUser.objects.get(matricula=matricula)
            print(f"[OK] CustomUser: {aluno.user.username} | Disciplina: {disciplina.nome}")

            print("[BUSCA] Procurando certificado correspondente...")
            certificado = get_object_or_404(Certificado, codigo=codigo, aluno=aluno, disciplina=disciplina)
            print(f"[OK] Certificado encontrado: {certificado.codigo}")

            nome = aluno.user.username
            percentual_acertos = certificado.percentual_acertos

            print("[GERAÇÃO] Preparando dados para o PDF...")
            data_formatada = converter_data_para_extenso(datetime.today())
            logo_path = os.path.join('static', 'img', 'logo', 'logo-teste.png')

            if not os.path.exists(logo_path):
                print(f"[AVISO] Logo não encontrado em: {logo_path}")
            else:
                print("[OK] Logo encontrado.")

            logo_base64 = converter_imagem_para_base64(logo_path)
            css_url = request.build_absolute_uri(static('css/certificado_pdf.css'))

            contexto = {
                "nome": nome.upper(),
                "data": data_formatada,
                "logo_base64": logo_base64,
                "percentual_acertos": percentual_acertos,
                "css_url": css_url,
            }

            print("[GERAÇÃO] Renderizando HTML do certificado...")
            rendered = render(request, 'certificado_pdf.html', contexto).content.decode('utf-8')
            print("[OK] HTML renderizado.")

            pdf_path = f'certificado_{nome.replace(" ", "_")}.pdf'
            print(f"[PDFKIT] Gerando PDF em: {pdf_path}")
            pdfkit.from_string(rendered, pdf_path, options={'enable-local-file-access': ''})

            if not os.path.exists(pdf_path):
                print("[ERRO] PDF não foi gerado corretamente!")
                return Response({'erro': 'Erro ao gerar o PDF.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            tamanho_pdf = os.path.getsize(pdf_path)
            print(f"[OK] PDF gerado com sucesso ({tamanho_pdf} bytes)")

            print("[RESPOSTA] Preparando envio do arquivo ao cliente...")
            response = FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=os.path.basename(pdf_path))
            response['Content-Type'] = 'application/pdf'

            print("[SUCESSO ✅] PDF pronto para download!\n=====================================================================")
            return response

        except Certificado.DoesNotExist:
            print("[ERRO] Certificado não encontrado ou dados inválidos.\n=====================================================================")
            return Response(
                {'erro': 'Certificado não encontrado ou dados inválidos.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"[EXCEÇÃO] Erro inesperado: {e}\n=====================================================================")
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CertificadoDetailView(APIView):
#     """
#     View para obter detalhes de um certificado específico.
#     """
#     permission_classes = [AllowAny]

#     def get(self, request, codigo):
#         if codigo:
#             try:
#                 certificado = Certificado.objects.get(codigo=codigo)
#                 serializer = CertificadoSerializer(certificado)
#                 return Response(serializer.data)
#             except Certificado.DoesNotExist:
#                 return Response({'erro': 'Certificado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'erro': 'Código do certificado não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)


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


def gerar_certificado_no_banco(data):
    """
    Gerar apenas se o aluno obteve pelo menos 70% de acertos
    """
    aluno = get_object_or_404(CustomUser, user__username=data['aluno'])
    disciplina = get_object_or_404(Disciplina, nome=data['disciplina'])

    Certificado.objects.get_or_create(
        aluno=aluno,
        disciplina=disciplina,
        percentual_acertos=data['acertos'],
        defaults={
            'codigo': gerar_codigo_certificado()
        }
    )

class CertificadoListView(APIView):
    """
    View para exibir a lista de certificados.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        certificados = Certificado.objects.all()
        serializer = CertificadoSerializer(certificados, many=True)
        return Response(serializer.data)
        

# configurar e criar o certificado
# def buscar_certificado():
#     pass

# def criar_pdf_certificado():
#     pass

# def baixar_certificado():
#     pass

# class CertificadoDownloadView(APIView):
#     """
#     View para gerar e baixar o certificado em PDF.
#     """
#     permission_classes = [AllowAny]
    
#     def get(self, request, codigo):
#         if codigo:
#             try:
#                 disciplina = Disciplina.objects.get(pk=1)
                
#                 certificado = get_object_or_404(Certificado, codigo=codigo, aluno=request.user.aluno, disciplina=disciplina)
#                 nome = request.user.username
#                 percentual_acertos = certificado.percentual_acertos

#                 data_formatada = converter_data_para_extenso(datetime.today())
#                 logo_path = os.path.join('static', 'img', 'logo', 'logo-teste.png')
                
#                 logo_base64 = converter_imagem_para_base64(logo_path)
#                 css_url = request.build_absolute_uri(static('css/certificado_pdf.css'))

#                 contexto = {
#                     "nome": nome.upper(),
#                     "data": data_formatada,
#                     "logo_base64": logo_base64,
#                     "percentual_acertos": percentual_acertos,
#                     'css_url': css_url
#                 }

#                 rendered = render(request, 'certificado_pdf.html', contexto).content.decode('utf-8')
#                 pdf_path = f'certificado_{nome.replace(" ", "_")}.pdf'
#                 pdfkit.from_string(rendered, pdf_path, options={'enable-local-file-access': ''})
                
#                 return FileResponse(open(pdf_path, 'rb'), as_attachment=True)
            
#             except Certificado.DoesNotExist:
#                 return Response({'erro': 'Certificado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'erro': 'Código do certificado não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)
