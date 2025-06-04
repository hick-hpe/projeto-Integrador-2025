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
- `GET /api/disciplinas/` - Listar disciplinas
- `GET /api/disciplinas/<int:disciplina_id>/quizzes/` - Listar os quizzes de uma disciplina
- `GET /api/quizzes/<int:quiz_id>/questoes/` - Listar as questões de um quiz
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
- `GET /api/certificados/<str:codigo>/` - Exibe os detalhes de um certificado. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "codigo": "CERT12345",
            "usuario": "Henrique",
            "disciplina": "Desenvolvimento Web II",
            "data_emissao": "2025-06-03"
        }
        ```
- `POST /api/quizzes/<int:quiz_id>/desistir/` - Informar à aplicação que o aluno desistiu do quiz: o servidor irá excluir os dados em cache
- `POST /api/quizzes/<int:quiz_id>/concluir/` - Informar à aplicação que o aluno concluiu do quiz: o servidor irá retornar o desempenho do aluno e excluir os dados em cache. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "chave": <int>
        }
        ```