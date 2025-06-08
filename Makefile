.PHONY: all git venv django start

all: git venv django start

git:
	@git config --global user.email ""
	@git config --global user.name "hick-hpe"
	@echo "----------------------"
	@echo "Autenticado!!!"
	@echo "----------------------"

start:
	@echo "Inicializando containers Docker..."
	@docker compose up --build -d

	@echo "Iniciando React..."
	@cd reactapp && \
	npm install && \
	npm run dev

