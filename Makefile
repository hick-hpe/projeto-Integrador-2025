.PHONY: all git start

all: git start

git:
	@git config --global user.email ""
	@git config --global user.name "hick-hpe"
	@echo "+---------------------+"
	@echo "|   Autenticado!!!   |"
	@echo "+---------------------+"

start:
	@echo "+----------------------------------------+"
	@echo "|  Inicializando containers Docker...    |"
	@echo "+----------------------------------------+"
	@docker compose up --build -d

