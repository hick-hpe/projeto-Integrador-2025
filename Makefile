.PHONY: all git venv django start

all: git venv django start

git:
	@git config --global user.email ""
	@git config --global user.name "hick-hpe"
	@echo "----------------------"
	@echo "Autenticado!!!"
	@echo "----------------------"

venv:
	@echo "Ativando ambiente virtual..."
	@. venv/bin/activate

django:
	@echo "Iniciando setup do Django..."
	@. venv/bin/activate && \
	cd devquiz && \
	pip install -r requirements.txt && \
	python manage.py makemigrations && \
	python manage.py migrate

start:
	@echo "Inicializando containers Docker..."
	@docker compose up --build
