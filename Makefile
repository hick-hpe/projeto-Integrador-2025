all: git start

git:
	@git config --global user.email ""
	@git config --global user.name "hick-hpe"
	@echo "----------------------"
	@echo "Autenticado!!!"
	@echo "----------------------\n"
	
# Diretórios
BACKEND_DIR=devquiz
FRONTEND_DIR=$(BACKEND_DIR)/reactapp
VENV_DIR=venv

# Variáveis
PYTHON_VENV=$(VENV_DIR)/bin/python

delete:
	@rm -rf projeto-Integrador-2025

# Clonar o repositório
clone:
	@git clone https://github.com/hick-hpe/projeto-Integrador-2025/
	@echo "----------------------"
	@echo "Repositório clonado!!!"
	@echo "----------------------\n"

# Criar ambiente virtual
venv:
	python3 -m venv $(VENV_DIR)
	@echo "-------------------------------------------"
	@echo "Ambiente virtual criado em $(VENV_DIR)"
	@echo "-------------------------------------------\n"

# Instalar dependências do backend (Python/Django)
deps:
	@echo "---- Conteúdo de projeto-Integrador-2025 ----"
	cd projeto-Integrador-2025 && \
	../$(VENV_DIR)/bin/pip install -r requirements.txt && \
	echo "----------------------------------" && \
	echo "Dependências Python instaladas!!!" && \
	echo "----------------------------------\n"

# Criar migrações e aplicar (Django)
migrate:
	@echo "------------ ls ------------"
	@ls projeto-Integrador-2025/$(BACKEND_DIR)
	@echo "------------ cd ------------"
	@cd projeto-Integrador-2025/$(BACKEND_DIR) \
	$(PYTHON_VENV) projeto-Integrador-2025/$(BACKEND_DIR)/manage.py makemigrations
	$(PYTHON_VENV) projeto-Integrador-2025/$(BACKEND_DIR)/manage.py migrate
	@echo "----------------------------------"
	@echo "Banco configurado com suceso!!!"
	@echo "----------------------------------\n"

# Rodar servidor Django
runserver:
	$(PYTHON_VENV) projeto-Integrador-2025/$(BACKEND_DIR)/manage.py runserver
	@echo "----------------------------------"
	@echo "Servidor Django On!!!"
	@echo "----------------------------------\n"

# Instalar dependências do React
frontend-install:
	cd $(FRONTEND_DIR) && npm install
	@echo "----------------------------------"
	@echo "Dependências React instaladas!!!"
	@echo "----------------------------------\n"

# Rodar servidor React
frontend-run:
	cd $(FRONTEND_DIR) && npm run dev
	@echo "----------------------------------"
	@echo "Dependências React instaladas!!!"
	@echo "Servidor react On!!!"
	@echo "----------------------------------\n"

# Rodar tudo (em terminais separados, manual)
start: delete clone venv deps migrate runserver frontend-run

# Limpar ambiente virtual
clean:
	rm -rf $(VENV_DIR)
	@echo "Servidor react On!!!"

.PHONY: clone venv deps migrate runserver frontend-install frontend-run start clean
