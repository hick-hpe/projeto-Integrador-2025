from django.contrib import admin
from .models import *

admin.site.register([
    Disciplina,
    Quiz,
    Questao,
    Alternativa,
    Emblema,
    Certificado
])

