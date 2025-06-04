# exemplos de como usar timedelta e datetime

from datetime import datetime, timedelta

# Data e hora atual
agora = datetime.now()
print('Agora:', agora)

# Adicionando 5 dias
cinco_dias = agora + timedelta(days=5)
print('Daqui a 5 dias:', cinco_dias)

# Subtraindo 2 horas
menos_duas_horas = agora - timedelta(hours=2)
print('Duas horas atrás:', menos_duas_horas)

# Diferença entre datas
data_futura = datetime(2025, 6, 10, 12, 0)
diferenca = data_futura - agora
print('Faltam', diferenca.days, 'dias e', diferenca.seconds // 3600, 'horas para 10/06/2025 12:00')

# Criando um timedelta de 1 semana e somando
uma_semana = timedelta(weeks=1)
semana_que_vem = agora + uma_semana
print('Daqui a uma semana:', semana_que_vem)