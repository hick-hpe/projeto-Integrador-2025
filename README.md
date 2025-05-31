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
- `GET /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Exibe os seguintes detalhes de uma questão:
    - Descrição
    - Alternativas
- `POST /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Recebe a repsosta do aluno de uma questão
- `GET /api/certificados/<str:codigo>/` - Exibe os seguintes detalhes de um certificado:
    - Código
    - Usuário
    - Disciplina
    - Data de emissão