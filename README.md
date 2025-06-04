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
- `GET /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Exibe os detalhes de uma questão. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "chave": <int>
        }
        ```
    - Descrição
    - Alternativas
- `POST /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Recebe a resposta do aluno de uma questão. <br/>
    - Formato de envio: <br/>
        ```
        {
            "alternativa_id": <int>
        }
        ```
    - Formato de resposta: <br/>
        ```
        {
            "chave": <int>
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