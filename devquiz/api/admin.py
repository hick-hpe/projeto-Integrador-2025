from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([
    Disciplina,
    Quiz,
    Questao,
    Alternativa,
    Pontuacao, # a ver...
    Certificado
])
