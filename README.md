# 🎓 Projeto Integrador - 2025

O **DevQuiz** é uma plataforma online de quizzes criada para ajudar estudantes de TADS a reforçar os conteúdos da graduação por meio de gamificação. Permite praticar, avaliar conhecimentos e acompanhar a evolução com certificação digital. Uma solução flexível, acessível e que potencializa o aprendizado de forma prática.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django, Django REST Framework  
- **Frontend:** React.js, Vite (em desenvolvimento)
- **Banco de Dados:** SQLite
- **Containerização:** Docker, Docker Compose  
- **Autenticação:** JWT (JSON Web Tokens)  
- **Controle de Versão:** Git e GitHub

## 🎯 Funcionalidades
- Realização de quizzes
- Quizzes divididos em três níveis:
    - Iniciante
    - Intermediário
    - Avançado
- Emissão de certificados para os alunos
- Registro de desempenho
- Gestão de disciplinas e quizzes
- Emblemas para cada nível de quiz aprovado

## 🚀 Funcionalidades futuras
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

## 📡 Teste da API
- 🚀 `GET /api/` – Testar disponibilidade da API.  
    - 📤 Formato de resposta:
        ```
        {
            "message": "api on!!"
        }
        ```

## 🔐 Autenticação
- 🆕 **CRIAR CONTA**
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
- 🔑 **FAZER LOGIN**
    > Nota: a sessão do usuário permanece por 1h.
    
    - 🚀 `POST /auth/login/` – Realizar o login na conta  
    - 📥 **Formato de envio:**  
        ```json
        {
            "username": "username",
            "password": "password"
        }
        ```
    - 📤 **Formato de resposta de sucesso:**  
        ```json
        {
            "detail": "Login realizado com sucesso!!"
        }
        ```

- ✏️ **ATUALIZAR DADOS DA CONTA**
    - 🚀 `PATCH /auth/conta/` – Editar dados da conta  
    - 📥 **Formato de envio:**  
        ```json
        {
            "username": "username",
            "email": "email", 
            "password": "password"
        }
        ```
    - 📤 **Formato de resposta de sucesso:**  
        ```json
        {
            "detail": "Dados atualizados com sucesso!!"
        }
        ```

- ❌ **EXCLUIR CONTA**
    - 🚀 `DELETE /auth/conta-detail/` – Excluir a conta  
    - 📤 **Formato de resposta de sucesso:**  
        ```json
        {
            "detail": "Conta excluída com sucesso!!"
        }
        ```

- 🔒 **LOGOUT**
    - 🚀 `POST /auth/logout/` – Encerra a sessão  
    - 📤 **Formato de resposta de sucesso:**  
        ```json
        {
            "detail": "Logout realizado com sucesso!!"
        }
        ```

## 🔌 Rotas da API

### 🎓 Rotas para Aluno
> Para usar a API, é necessário estar autenticado!

- 📚 `GET /api/disciplinas/` – Listar disciplinas  
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 1,
                "nome": "Desenvolvimento Web II"
            }
        ]
        ```

- 📝 `GET /api/quizzes/` – Listar quizzes
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 1,
                "titulo": "POO - Conceitos Básicos",
                "disciplina": "POO",
                "tipo_questoes": "Múltipla Escolha",
                "nivel": "Iniciante",
                "descricao": "Fundamentos iniciais de Programação Orientada a Objetos.",
                "questoes": [
                    {
                        "id": 1,
                        "descricao": "O que é uma classe em POO?",
                        "alternativas": [
                            {
                                "id": 1,
                                "texto": "Um molde/estrutura para criar objetos."
                            },
                            {
                                "id": 2,
                                "texto": "Um objeto já instanciado."
                            },
                            {
                                "id": 3,
                                "texto": "Um tipo de banco de dados."
                            }
                        ]
                    }
                ]
            }
        ]
        ```

- ❓ `GET /api/quizzes/<int:quiz_id>/questoes/` – Listar questões de um quiz - 10 aleatoriamente
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 2,
                "descricao": "O que é um objeto?",
                "alternativas": [
                    {
                        "id": 4,
                        "texto": "Uma instância de uma classe."
                    },
                    {
                        "id": 5,
                        "texto": "Um tipo de variável global."
                    },
                    {
                        "id": 6,
                        "texto": "Um método especial da classe."
                    }
                ]
            }
        ]
        ```

- 📝 `GET /api/quizzes/<int:quiz_id>/aluno-pode-fazer/` - Verificar se o aluno pode fazer o quiz
    - 📤 **Formato de resposta:**
        Caso seja um nível superior ao qual o aluno não respondeu ainda, bloqueado!
        ```json
        {
            "detail": "Você não pode fazer o nível Avançado!"
        }
        ```
        Ou
        ```json
        {
            "detail": "Você não pode fazer o nível Intermediário!"
        }
        ```

        Caso puder, OK!
        ```json
        {
            "detail": "OK"
        }
        ```

- 📝 `POST /api/quizzes/<int:quiz_id>/`- Informações do quiz
    - 📥 **Formato de envio:**  
        ```json
        {
            "id": 1,
            "titulo": "POO - Conceitos Básicos",
            "disciplina": "POO",
            "tipo_questoes": "Múltipla Escolha",
            "nivel": "Iniciante",
            "descricao": "Fundamentos iniciais de Programação Orientada a Objetos.",
            "questoes": [
                {
                    "id": 1,
                    "descricao": "O que é uma classe em POO?",
                    "alternativas": [
                        {
                            "id": 1,
                            "texto": "Um molde/estrutura para criar objetos."
                        },
                        {
                            "id": 2,
                            "texto": "Um objeto já instanciado."
                        },
                        {
                            "id": 3,
                            "texto": "Um tipo de banco de dados."
                        }
                    ]
                }
            ]
        }
        ```

- 📝 `GET /api/quizzes/<int:quiz_id>/respostas-ultimo-quiz/` - Exibir as respostas do aluno no último quiz
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 10,
                "aluno": 1,
                "questao": 1,
                "alternativa": 1
            },
            {
                "id": 11,
                "aluno": 1,
                "questao": 2,
                "alternativa": 6
            },
            {
                "id": 12,
                "aluno": 1,
                "questao": 3,
                "alternativa": 9
            }
        ]
        ```

- 📝 `GET /api/quizzes/<int:quiz_id>/questoes/respostas-corretas/` - Exibir as respostas das perguntas repsondidas pelo aluno (gabarito)
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 1,
                "descricao": "O que é uma classe em POO?",
                "alternativas": [
                    {
                        "id": 1,
                        "texto": "Um molde/estrutura para criar objetos."
                    },
                    {
                        "id": 2,
                        "texto": "Um objeto já instanciado."
                    },
                    {
                        "id": 3,
                        "texto": "Um tipo de banco de dados."
                    }
                ],
                "resposta_correta": 1,
                "explicacao": null
            }
        ]
        ```

- 🖊️ `POST /api/quizzes/<int:quiz_id>/questoes/<int:questao_id>/responder/` – Enviar resposta do aluno
    - 📤 **Formato de resposta:**  
        ```json
        {
            "questao": "Descrição",
            "resposta_aluno": "Texto fa alternativa escolhida",
            "detail": "Resposta registrada com sucesso."
        }
        ```

        Caso não tenha iniciado o quiz:
        ```json
        {
            "detail": "Nenhuma tentativa ativa encontrada para este quiz."
        }
        ```

        Caso já tenha repsondido nesta tentativa:
        ```json
        {
            "questao": "Descrição",
            "resposta_aluno": "Texto fa alternativa escolhida",
            "detail": "Você já respondeu esta questão nesta tentativa."
        }
        ```

- 🏁 `POST /api/quizzes/<int:quiz_id>/iniciar/` – Indica que o aluno iniciou o quiz  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "detail": "ok"
        }
        ```
        Caso tente de novo, status 400
        ```json
        {
            "detail": "Este quiz já foi iniciado e ainda não foi concluído"
        }
        ```

- 🏳️ `POST /api/quizzes/<int:quiz_id>/desistir/` – Indica que o aluno desistiu do quiz e limpa os dados temporários  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "mensagem": "Você desistiu do quiz!"
        }
        ```

        Caso tente desisitr de um quiz não iniciado:
        ```json
        {
            "detail": "Nenhuma tentativa ativa para desistir."
        }
        ```

- 🏁 `POST /api/quizzes/<int:quiz_id>/concluir/` – Exibe o desempenho do aluno no quiz  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "detail": "Quiz concluído com sucesso",
            "acertos": 3,
            "total_questoes": 10,
            "porcentagem": 33.33,
            "aprovado": false
        }
        ```

        Caso não tenha iniciado um quiz:
        ```json
        {
            "detail": "Nenhuma tentativa ativa encontrada."
        }
        ```

### Emblemas
- 🏅 `GET /api/emblemas/` – Mostra os emblemas disponíveis  
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 1,
                "nome": "Primeiro Quiz",
                "descricao": "Concluiu o primeiro quiz na plataforma.",
                "disciplina": "Matemática"
            }
        ]
        ```

- 🏆 `GET /api/emblemas/aluno/` – Mostra os emblemas conquistados pelo usuário  
    - 📤 **Formato de resposta:**  
        ```json
        [
            {
                "id": 1,
                "emblema": {
                    "id": 4,
                    "nome": "Iniciante POO",
                    "descricao": "Emblema concedido ao completar o quiz iniciante de Programação Orientada a Objetos.",
                    "disciplina": "POO"
                },
                "conquistado_em": "2025-11-30T22:17:41.075468-03:00"
            }
        ]
        ```

### Certificados
- 📜 `GET /api/certificados/` – Faz a validação de um certificado
    - 📤 **Formato de resposta:**  
        ```json
        {
            "valido": true,
        }
        ```

- 📜 `GET /api/certificados/<str:codigo>/download/` – Faz o download do certificado do aluno logado
    - 📤 **Formato de resposta:**  
        - 📕 Um arquivo PDF

- 📜 `GET /api/certificados/validar-certificado/` – Faz a validação de um certificado  
    - 📤 **Formato de envio:**
        ```json
        {
            "codigo": "CERT12345",
            "matricula": "12345678"
        }
        ```

    - 📤 **Formato de resposta:**  
        ```json
        {
            "valido": true,
        }
        ```

<!-- ### ⚙️ Rotas para admin/moderador
Para isso, deve estar logado como admin/moderador.

- 📚 `GET /api/adm/disciplinas/` – Listar todas as disciplinas  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "id": 1,
            "nome": "web"
        }
        ```

- 🔍 `GET /api/adm/disciplinas/<int:id>/` – Obter dados de uma disciplina  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "id": 1,
            "nome": "web"
        }
        ```

- 🆕 `POST /api/adm/disciplinas/` – Criar uma disciplina  
    - 📥 **Formato de envio:**  
        ```json
        {
            "nome": "Nova disciplina"
        }
        ```
    - 📤 **Formato de resposta:**  
        ```json
        {
            "message": "Disciplina criada com sucesso!"
        }
        ```

- ✏️ `PATCH /api/adm/disciplinas/<int:id>/` – Atualizar dados de uma disciplina  
    - 📥 **Formato de envio:**  
        ```json
        {
            "nome": "Novo nome"
        }
        ```
    - 📤 **Formato de resposta:**  
        ```json
        {
            "message": "Disciplina atualizada com sucesso!"
        }
        ```

- ❌ `DELETE /api/adm/disciplinas/<int:id>/` – Excluir disciplina  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "message": "Disciplina excluída com sucesso!"
        }
        ```

- 📋 `GET /api/adm/quizzes/` – Listar todos os quizzes criados  
    - 📤 **Formato de resposta:**  
        ```json
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
                            {"id": 1, "texto": "Python"},
                            {"id": 2, "texto": "JavaScript"},
                            {"id": 3, "texto": "SQL"},
                            {"id": 4, "texto": "PHP"}
                        ]
                    }
                ]
            }
        ]
        ```

- 🔍 `GET /api/adm/quizzes/<int:id>/` – Obter dados de um quiz  
    - 📤 **Formato de resposta:**  
        ```json
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
                        {"id": 1, "texto": "Python"},
                        {"id": 2, "texto": "JavaScript"},
                        {"id": 3, "texto": "SQL"},
                        {"id": 4, "texto": "PHP"}
                    ]
                }
            ]
        }
        ```

- 🆕 `POST /api/adm/quizzes/` – Criar um quiz  
    - 📥 **Formato de envio:**  
        ```json
        {
            "descricao": "Learn how to create, read, update, and delete quizzes using a RESTful API built with Django REST Framework.",
            "disciplina": "API Development",
            "nivel": "Intermediate",
            "questoes": [
                {
                    "descricao": "Which HTTP method is used to create a new quiz in a RESTful API?",
                    "alternativas": ["GET", "POST", "PUT", "DELETE"],
                    "resposta_correta": "POST",
                    "explicacao": "The POST method is used to create new resources in a RESTful API."
                }
            ]
        }
        ```
    - 📤 **Formato de resposta:**  
        ```json
        {
            "message": "Quiz criado com sucesso!"
        }
        ```

- ✏️ `PATCH /api/adm/quizzes/<int:id>/` – Editar um quiz  
    - 📥 **Formato de envio:**  
        ```json
        {
            "descricao": "Texto atualizado"
        }
        ```
    - 📤 **Formato de resposta:**  
        ```json
        {
            "message": "Quiz atualizado com sucesso!"
        }
        ```

- ❌ `DELETE /api/adm/quizzes/<int:id>/` – Excluir um quiz  
    - 📤 **Formato de resposta:**  
        ```json
        {
            "message": "Quiz excluído com sucesso!"
        }
        ``` -->

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

