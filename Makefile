all: git start

git:
	@git config --global user.email ""
	@git config --global user.name "hick-hpe"
	@echo "----------------------"
	@echo "Autenticado!!!"
	@echo "----------------------\n"

start:
	docker compose up --build

.PHONY: all git start
