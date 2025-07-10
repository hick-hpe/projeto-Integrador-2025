# Projeto Integrador - 2025

O **DevQuiz** é uma plataforma online de quizzes desenvolvida para apoiar os alunos do curso de Tecnologia em Análise e Desenvolvimento de Sistemas (TADS) na fixação dos conteúdos abordados durante o curso. A proposta do DevQuiz é baseada em estudos que comprovam a eficácia da gamificação como ferramenta para aumentar o engajamento e a motivação dos estudantes.

Ao oferecer quizzes interativos, o DevQuiz estimula a aprendizagem ativa, permitindo que os alunos testem seus conhecimentos de forma contínua e prática. Esse método auxilia na identificação de pontos que precisam ser reforçados, tornando o estudo mais focado e eficiente. Além disso, a diversidade dos níveis de dificuldade (iniciante, intermediário e avançado) atende a diferentes perfis de alunos, respeitando seu ritmo e conhecimento prévio.

A plataforma também oferece a emissão de certificados digitais, que atestam a conclusão dos quizzes e o esforço dos alunos dentro do ambiente do DevQuiz. Esses certificados funcionam como um incentivo interno e ferramenta de autoavaliação, sem caráter oficial ou validade reconhecida externamente. O formato online possibilita acesso fácil e flexível, permitindo que o estudo ocorra a qualquer momento e lugar, adequando-se à rotina dos estudantes.

Por fim, o DevQuiz representa uma inovação na forma de ensino, diversificando os métodos tradicionais e potencializando os resultados do aprendizado, além de ter grande potencial de escalabilidade para outros cursos e áreas.

## Funcionalidades
<!-- - Criação de quizzes (em desenvolvimento) -->
- Realização de quizzes
- Quizzes divididos em três níveis:
    - Iniciante
    - Intermediário
    - Avançado
- Emissão de certificados para os alunos

## Funcionalidades futuras
- Sistema de ranking entre os participantes
- Emblemas sugeridos:
  - **Conclusão de Nível**: Recebido ao completar todos os quizzes de um nível (Iniciante, Intermediário, Avançado)
  - **Sequência de Acertos**: Para quem acerta um número X de perguntas seguidas sem errar
  - **Participação Frequente**: Concedido a usuários que realizam quizzes diariamente por um período contínuo (ex: 7 dias)
- **Especialista em Disciplina**: Recebido ao concluir com sucesso todos os quizzes de uma disciplina específica (níveis Iniciante, Intermediário e Avançado).
  - **Primeiro Quiz**: Recebido ao completar o primeiro quiz na plataforma
  <!-- - **Top do Ranking**: Para os usuários que alcançam as melhores posições no sistema de ranking -->
- Notificações visuais para conquistas, como pop-ups ou animações ao ganhar um emblema
- Área dedicada no perfil do usuário para exibição dos emblemas conquistados
<!-- - Possibilidade de compartilhar conquistas em redes sociais para aumentar o engajamento -->


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
    - Iniciar container docker:
        ```
        docker compose up
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