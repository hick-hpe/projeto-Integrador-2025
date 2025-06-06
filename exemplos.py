from datetime import datetime, timedelta

data = datetime(2025, 6, 3)

# formatar em dd/MM/YYYY
print(data.strftime('%d/%m/%Y'))  # Saída: 03/06/2025
print(data.day)