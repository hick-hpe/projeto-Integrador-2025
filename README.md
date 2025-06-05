# Projeto Integrador - 2025

O projeto DevQuiz é um site de quizzes, voltado aos alunos do curso de TADS, com o objetivo de complementar os estudos dos alunos.

## Funcionalidades
- Criação de quizzes
- Realização de quizzes
- Quizzes divididos em três níveis:
    - Iniciante
    - Intermediário
    - Avançado
- Emissão de certificados para os alunos
- Futuramente, espera-se implementar uma funcionalidade de ranking

## Rotas da API
- `GET /api/disciplinas/` - Listar disciplinas. <br/>
    - Formato de resposta: <br/>
        ```
        [
            {
                "id": 1,
                "nome": "Desenvolvimento Web II"
            }
        ]
        ```
- `GET /api/disciplinas/<int:disciplina_id>/quizzes/` - Listar os quizzes de uma disciplina. <br/>
    - Formato de resposta: <br/>
        ```
        [
            {
                "id": 1,
                "disciplina": "Desenvolvimento Web II",
                "nivel": "Iniciante",
                "descricao": "Quiz sobre conceitos básicos de Django."
            }
        ]
        ```
- `GET /api/quizzes/<int:quiz_id>/questoes/` - Listar as questões de um quiz. <br/>
    - Formato de resposta: <br/>
        ```
        [
            {
                "id": 51,
                "quiz": 3,
                "descricao": "Django é um framework web escrito em Python.",
                "alternativas": [
                    {
                        "id": 29,
                        "texto": "Verdadeiro"
                    },
                    {
                        "id": 30,
                        "texto": "Falso"
                    }
                ]
            }
        ]
        ```
- `GET /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Exibe os detalhes de uma questão. Pde ser em múltipla escolha ou verdadeiro e falso. <br/>
    - Formato de resposta de Verdadeiro/Falso: <br/>
        ```
        {
            "id": 57,
            "quiz": 3,
            "descricao": "Descrição da questão aqui",
            "alternativas": [
                {
                    "id": 45,
                    "texto": "Verdadeiro"
                },
                {
                    "id": 46,
                    "texto": "Falso"
                }
            ]
        }
        ```
    - Formato de resposta de Múltipla Escolha: <br/>
        ```
        {
            "id": 58,
            "quiz": 3,
            "descricao": "Descrição da questão aqui",
            "alternativas": [
                {
                    "id": 47,
                    "texto": "Aternativa 1"
                },
                {
                    "id": 48,
                    "texto": "Aternativa 2"
                },
                {
                    "id": 49,
                    "texto": "Aternativa 3"
                },
                {
                    "id": 50,
                    "texto": "Aternativa 4"
                }
            ]
        }
        ```
- `GET /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/resposta/` - Exibe a resposta da questão e sua explicação. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "detail": {
                "id": 17,
                "questao": "Descrição da questão aqui",
                "alternativa": "Verdadeiro",
                "explicacao": "Explicação aqui"
            }
        }
        ```
- `POST /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Recebe a resposta do aluno de uma questão. <br/>
    - Formato de envio: <br/>
        ```
        {
            "alternativa_id": 12
        }
        ```
    - Formato de resposta: <br/>
        ```
        {
            "correto": false,
            "id": 18,
            "questao": "Descrição da questão aqui",
            "alternativa": "Descrição da alternativa aqui",
            "explicacao": "Explicação da reposta"
        }
        ```
- `GET /certificados/<str:codigo>/` - Exibe os detalhes de um certificado. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "codigo": "CERT12345",
            "usuario": "Henrique",
            "disciplina": "Desenvolvimento Web II",
            "data_emissao": "2025-06-03"
        }
        ```
- `POST /api/quizzes/<int:quiz_id>/desistir/` - Informar à aplicação que o aluno desistiu do quiz e limpa os dados temporários. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "mensagem": "Você desistiu do quiz!"
        }
        ```
- `POST /api/quizzes/<int:quiz_id>/concluir/` - Mostra o desempenho do aluno no quiz. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "mensagem": "Quiz concluído com sucesso!",
            "usuario": "Henrique",
            "quiz": "iniciante",
            "disciplina": "Desenvolvimento Web II",
            "acertos": 4,
            "total_questoes": 10,
            "pontuacao": 40
        }
        ```
## Rodar protótipo teste:
- Instalação:
    - Clonar repositório:
        ```
        git clone https://github.com/hick-hpe/projeto-Integrador-2025/
        ```
    - Acessar o repositório:
        ```
        cd projeto-Integrador-2025
        ```
    - Criar e ativar ambiente virtual:
        - Windows:
            ```
            python -m venv venv
            venv\Scripts\activate
            ```
        - Linux/MacOS:
            ```
            python3 -m venv venv
            source venv/bin/activate
            ```
- Ambiente Django:
    - Instalar dependências:
        ```
        pip install -r requirements.txt
        ```
    - Acessar o projeto:
        ```
        cd devquiz
        ```
    - Criar as migrações:
        ```
        python manage.py makemigrations
        ```
    - Criar as tabelas:
        ```
        python manage.py migrate
        ```
    - Iniciar servidor:
        ```
        python manage.py runserver
        ```
- Ambiente React:
    - Acessar o projeto:
        ```
        cd devquiz/reactapp
        ```
    - Instalar dependências:
        ```
        npm install
        ```
    - Iniciar servidor:
        ```
        npm run dev
        ```
## Servidores
- Servidor Django:
    ```
    http://localhost:8000/
    ```
- Servidor React:
    ```
    http://localhost:5173/
    ```