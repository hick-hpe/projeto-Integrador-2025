# Usa uma imagem Python leve baseada em Debian
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /devquiz

# Instala dependências do sistema necessárias para o wkhtmltopdf e bibliotecas de renderização
RUN apt-get update && \
    apt-get install -y wkhtmltopdf libxrender1 libfontconfig1 libxext6 && \
    apt-get install -y curl && \
    apt-get clean

# Copia o arquivo de dependências do Python para o container
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

# Expõe a porta 8000 (usada pelo Gunicorn)
EXPOSE 8000

# Comando padrão: inicia o Gunicorn como servidor WSGI para produção
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "devquiz.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]