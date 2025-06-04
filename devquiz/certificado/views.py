from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import Certificado
from api.serializers import CertificadoSerializer
from rest_framework.permissions import AllowAny

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
    else:
        return Response({'erro': 'Código do certificado não fornecido.'}, status=400)

