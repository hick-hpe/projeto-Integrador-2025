from datetime import datetime
import pytz

# UTC agora
utc_now = datetime.now(pytz.utc)
print("UTC:", utc_now)

# Converter para horário de São Paulo
sp = utc_now.astimezone(pytz.timezone('America/Sao_Paulo'))
print("São Paulo:", sp)
