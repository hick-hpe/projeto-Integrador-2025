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

commit:
	@echo "+----------------------------------------+"
	@echo "|  Commitando alterações...              |"
	@echo "+----------------------------------------+"
	@bash -c 'read -p "Digite a mensagem do commit: " msg && \
              echo "Mensagem do commit: $$msg" && \
              git add . && \
              git commit -m "$$msg" && \
			  git branch -M main && \
			  git push'
	@echo "+----------------------------------------+"
	@echo "|     Commit realizado com sucesso!      |"
	@echo "+----------------------------------------+"
