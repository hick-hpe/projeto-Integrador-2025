# 🎓 Projeto Integrador - 2025

O **DevQuiz** é uma plataforma online de quizzes criada para ajudar estudantes de TADS a reforçar os conteúdos da graduação por meio de gamificação. Permite praticar, avaliar conhecimentos e acompanhar a evolução com certificação digital. Uma solução flexível, acessível e que potencializa o aprendizado de forma prática.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django, Django REST Framework  
- **Frontend:** React.js, Vite (em desenvolvimento)
- **Banco de Dados:** SQLite
- **Containerização:** Docker, Docker Compose  
- **Autenticação:** JWT (JSON Web Tokens)  
- **Controle de Versão:** Git e GitHub

## 🛠️ Funcionalidades
- Realização de quizzes
- Quizzes divididos em três níveis:
    - Iniciante
    - Intermediário
    - Avançado
- Emissão de certificados para os alunos
- Registro de desempenho
- Gestão de disciplinas e quizzes

## 🛠️ Funcionalidades futuras
- Sistema de ranking entre os participantes
- Emblemas sugeridos:
  - **Conclusão de Nível**: Recebido ao completar todos os quizzes de um nível (Iniciante, Intermediário, Avançado)
  - **Sequência de Acertos**: Para quem acerta um número X de perguntas seguidas sem errar
  - **Participação Frequente**: Concedido a usuários que realizam quizzes diariamente por um período contínuo (ex: 7 dias)
  - **Especialista em Disciplina**: Recebido ao concluir com sucesso todos os quizzes de uma disciplina específica (níveis Iniciante, Intermediário e Avançado).
  - **Primeiro Quiz**: Recebido ao completar o primeiro quiz na plataforma
  - **Quiz 100%**: Recebido ao completar um quiz com 100% de acertos na plataforma
  - **Top do Ranking**: Para os usuários que alcançam as melhores posições no sistema de ranking
- Notificações visuais para conquistas, como pop-ups ou animações ao ganhar um emblema
- Área dedicada no perfil do usuário para exibição dos emblemas conquistados
- Possibilidade de compartilhar conquistas em redes sociais para aumentar o engajamento

## 🔐 Autenticação
- 🆕 CRIAR CONTA
    - 🚀 `POST /auth/cadastro/` - Criar uma conta. <br/>
        - 📥 Formato de envio: <br/>
            ```
            {
                "username": "username",
                "email": "email",
                "password": "password",
                "confirm-password": "confirm-password"
            }
            ```
        - 📤 Formato de resposta de sucesso: <br/>
            ```
            {
                "detail": "Conta criada com sucesso!!"
            }
            ```
        - 📤 Formato de resposta de erro de usuário criado: <br/>
            ```
            {
                "error": "Este usuário já existe!"
            }
            ```
        - 📤 Formato de resposta de erro na senha: <br/>
            ```
            {
                "error": "As senhas não coindizem!"
            }
            ```
        - 📤 Formato de resposta de erro de dados faltantes: <br/>
            ```
            {
                "error": "Preencha os campos!"
            }
            ```
- FAZER LOGIN
    - `POST /auth/login/` - Realizar o login na conta. <br/>
        - Formato de envio: <br/>
        ```
        {
            "username": "username",
            "password": "password"
        }
        ```
    - Formato de resposta de sucesso: <br/>
        ```
        {
            "detail": "Login realizado com sucesso!!"
        }
        ```
- ATUALIZAR DADOS DA CONTA
    - `PUT /auth/conta-detail/` - Editar dados da conta
        - Formato de envio: <br/>
        ```
        {
            "username": "username",
            "email": "email", 
            "password": "password"
        }
        ```
    - Formato de resposta de sucesso: <br/>
        ```
        {
            "detail": "Dados atualizados com sucesso!!"
        }
        ```
- EXCLUIR CONTA
    - `DELETE /auth/conta-detail/` - Excluir a conta.
    - Formato de resposta de sucesso: <br/>
        ```
        {
            "detail": "Conta excluída com sucesso!!"
        }
        ```

- LOGOUT
    - `POST /auth/logout/` - Encerra a sessão.
    - Formato de resposta de sucesso: <br/>
        ```
        {
            "detail": "Logout realizado com sucesso!!"
        }
        ```

- ENVIAR EMAIL
    - `POST /auth/enviar-email/` - Envia um código de recuperação de conta para o email cadastrado no sistema.
    - Formato de envio: <br/>
        ```
        {
            "email": "email"
        }
        ```
    - Formato de resposta de sucesso: <br/>
        ```
        {
            "detail": "Código enviado com sucesso!!"
        }
        ```

- VALIDAR CÓDIGO
    - `POST /auth/validar-codigo/` - Verifica se código informado foi o mesmo que foi enviado para o email do usuário.
    - Formato de envio: <br/>
        ```
        {
            "email": "email",
            "codigo": "codigo"
        }
        ```
    - Formato de resposta de sucesso: <br/>
        ```
        {
            "detail": "Código enviado com sucesso!!"
        }
        ```

## 🔌 Rotas da API
### Rotas para Aluno
Para usar a API, deve estar autenticado!
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
- `GET /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/` - Exibe os detalhes de uma questão. Pode ser em múltipla escolha ou verdadeiro e falso. <br/>
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
- `POST /api/quizzes/<int:quiz_id>/iniciar/` - Informar à aplicação que o aluno iniciou do quiz e preparar para salvar os dados. <br/>
    - Formato de resposta: <br/>
        ```
        {
            "mensagem": "Você iniciou do quiz!"
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
- `GET /api/emblemas/` - Mostrar todos os emblemas disponíveis.
    - Formato de resposta: <br/>
        ```
        [
            {
                "nome": "Primeiro Quiz",
                "descricao": "Concluiu o primeiro quiz na plataforma.",
                "logo": "/caminho/da/logo.png"
            }
        ]
        ```

- `GET /api/emblemas/user/<str:username>/` - Mostrar os emblemas conquistados pelo usuário.
    - Formato de resposta: <br/>
        ```
        [
            {
                "nome": "Primeiro Quiz",
                "descricao": "Concluiu o primeiro quiz na plataforma.",
                "logo": "/caminho/da/logo.png"
            }
        ]
        ```

### Rotas para admin/moderador
Para isso, deve estar logado como admin/moderador.

- `GET /api/adm/disciplinas/` - Listar todas as disciplinas
    - Formato de resposta: <br/>
        ```
        {
            "id": 1,
            "nome": "web"
        }
        ```

- `GET /api/adm/disciplinas/<int:id>/` - Obter dados de uma disciplina
    - Formato de resposta: <br/>
        ```
        {
            "id": 1,
            "nome": "web"
        }
        ```

- `POST /api/adm/disciplinas/` - Cria uma disciplina
    - Formato de envio: <br/>
        ```
        {
            "nome": "Nova disciplina"
        }
        ```
    - Formato de resposta: <br/>
        ```
        {
            "message": "Disciplina criada com sucesso!"
        }
        ```

- `PATCH /api/adm/disciplinas/<int:id>/` - Atualizar dados de uma disciplina
    - Formato de envio: <br/>
        ```
        {
            "nome": "Novo nome"
        }
        ```
    - Formato de resposta: <br/>
        ```
        {
            "message": "Disciplina atualizada com sucesso!"
        }
        ```

- `DELETE /api/adm/disciplinas/<int:id>/` - Excluir disciplina
    - Formato de resposta: <br/>
        ```
        {
            "message": "Disciplina excluída com sucesso!"
        }
        ```

- `GET /api/adm/quizzes/` - Listar todos os quizzes criados
    - Formato de resposta: <br/>
        ```
        [
            {
                "id": 1,
                "disciplina": "web",
                "nivel": "Iniciante",
                "descricao": "Quiz para iniciantes em desenvolvimento web",
                "questoes": [
                    {
                        "id": 1,
                        "quiz": 1,
                        "descricao": "Qual das seguintes linguagens é utilizada principalmente no lado do cliente para tornar as páginas web interativas?",
                        "alternativas": [
                            {
                                "id": 1,
                                "texto": "Python"
                            },
                            {
                                "id": 2,
                                "texto": "JavaScript"
                            },
                            {
                                "id": 3,
                                "texto": "SQL"
                            },
                            {
                                "id": 4,
                                "texto": "PHP"
                            }
                        ]
                    }
                ]
            }
        ]
        ```

- `GET /api/adm/quizzes/<int:id>/` - Obter dados de um quiz
    - Formato de resposta: <br/>
        ```
        {
            "id": 1,
            "disciplina": "web",
            "nivel": "Iniciante",
            "descricao": "Quiz para iniciantes em desenvolvimento web",
            "questoes": [
                {
                    "id": 1,
                    "quiz": 1,
                    "descricao": "Qual das seguintes linguagens é utilizada principalmente no lado do cliente para tornar as páginas web interativas?",
                    "alternativas": [
                        {
                            "id": 1,
                            "texto": "Python"
                        },
                        {
                            "id": 2,
                            "texto": "JavaScript"
                        },
                        {
                            "id": 3,
                            "texto": "SQL"
                        },
                        {
                            "id": 4,
                            "texto": "PHP"
                        }
                    ]
                }
            ]
        }
        ```

- `POST /api/adm/quizzes/` - Criar um quiz
    - Formato de envio:
        ```
        {
            "descricao": "Learn how to create, read, update, and delete quizzes using a RESTful API built with Django REST Framework.",
            "disciplina": "API Development",
            "nivel": "Intermediate",
            "questoes": [
                {
                    "descricao": "Which HTTP method is used to create a new quiz in a RESTful API?",
                    "alternativas": [
                        "GET",
                        "POST",
                        "PUT",
                        "DELETE"
                    ],
                    "resposta_correta": "POST",
                    "explicacao": "The POST method is used to create new resources in a RESTful API."
                }
            ]
        }
        ```
    - Formato de resposta:
        ```
        {
            "message": "Quiz criado com sucesso!"
        }
        ```
- `PATCH /api/adm/quizzes/<int:id>/` - Editar um quiz
    - Formato de envio: <br/>
        ```
        {
            "descricao": "Texto atualizado"
        }
        ```
    - Formato de resposta: <br/>
        ```
        {
            "message": "Quiz atualizado com sucesso!"
        }
        ```
- `DELETE /api/adm/quizzes/<int:id>/` - Excluir um quiz
    - Formato de resposta: <br/>
        ```
        {
            "message": "Quiz excluído com sucesso!"
        }
        ```

## 🚀 Rodar protótipo de teste

- 🔧 **Instalação:**
    - 📂 Clonar repositório:
        ```
        git clone https://github.com/hick-hpe/projeto-Integrador-2025/
        ```
    - 📁 Acessar o repositório:
        ```
        cd projeto-Integrador-2025
        ```
    - 🔐 Adicionar variáveis de ambiente:
        - 🗄️ backend/.env:
            ```bash
            EMAIL_HOST_USER='email'
            EMAIL_HOST_PASSWORD='senha de app'
            ```
        - 🌐 frontend/.env:
            ```bash
            VITE_REACT_APP_API_URL=http://localhost:8000/api/
            ```
    - ▶️ Executar:
        ```bash
        docker compose up
        ```

## 🌍 Servidores
- 🐍 **Servidor Django**:
    ```
    http://localhost:8000/
    ```
- ⚛️ **Servidor React**:
    ```
    http://localhost:5173/
    ```

> ⚠️ **Nota:** devido à configuração dos cookies, ambos os servidores precisam estar no mesmo domínio!


<!-- ## Como Contribuir

Contribuições são bem-vindas! Para contribuir com o DevQuiz:

1. Faça um fork do projeto  
2. Crie uma branch para sua feature ou correção (`git checkout -b minha-feature`)  
3. Faça commit das suas alterações (`git commit -m "Descrição da feature"`)  
4. Envie para seu fork (`git push origin minha-feature`)  
5. Abra um Pull Request aqui no repositório original  
6. Aguarde a revisão e feedback dos mantenedores -->

---

<!-- ## Contato

Em caso de dúvidas ou sugestões, entre em contato com:

- Henrique Palermo – [e-mail@example.com](mailto:e-mail@example.com)  
- GitHub: [https://github.com/hick-hpe](https://github.com/hick-hpe)   -->

