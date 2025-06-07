from devquiz.api.models import *
from django.contrib.auth.models import User

# Busca ou cria a disciplina
disciplina, _ = Disciplina.objects.get_or_create(nome='Desenvolvimento Web II')

# Apaga todas as questões existentes para evitar duplicação
for q in Questao.objects.all():
    q.delete()

# Cria os 3 quizzes por nível
quiz_iniciante, _ = Quiz.objects.get_or_create(disciplina=disciplina, nivel="Iniciante")
quiz_intermediario, _ = Quiz.objects.get_or_create(disciplina=disciplina, nivel="Intermediário")
quiz_avancado, _ = Quiz.objects.get_or_create(disciplina=disciplina, nivel="Avançado")

# Questões para cada nível
questoes_iniciante = [
    {
        'descricao': 'Django é um framework web escrito em Python.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual arquivo define as configurações principais do projeto Django?',
        'alternativas': [
            {'texto': 'urls.py', 'correta': False},
            {'texto': 'settings.py', 'correta': True},
            {'texto': 'models.py', 'correta': False},
            {'texto': 'views.py', 'correta': False},
        ],
    },
    {
        'descricao': 'O que o comando "python manage.py runserver" faz?',
        'alternativas': [
            {'texto': 'Inicia o servidor de desenvolvimento Django', 'correta': True},
            {'texto': 'Cria o banco de dados', 'correta': False},
            {'texto': 'Apaga as migrações', 'correta': False},
            {'texto': 'Cria um novo app', 'correta': False},
        ],
    },
    {
        'descricao': 'Em Django, o que é um "app"?',
        'alternativas': [
            {'texto': 'Uma aplicação completa, como um site inteiro', 'correta': False},
            {'texto': 'Um componente modular que faz parte do projeto Django', 'correta': True},
            {'texto': 'Um banco de dados', 'correta': False},
            {'texto': 'Um template HTML', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual comando é usado para criar migrações após alterar modelos?',
        'alternativas': [
            {'texto': 'python manage.py migrate', 'correta': False},
            {'texto': 'python manage.py makemigrations', 'correta': True},
            {'texto': 'python manage.py runserver', 'correta': False},
            {'texto': 'python manage.py startapp', 'correta': False},
        ],
    },
    {
        'descricao': 'O que é o ORM do Django?',
        'alternativas': [
            {'texto': 'Um gerenciador de banco de dados externo', 'correta': False},
            {'texto': 'Uma ferramenta para criar templates HTML', 'correta': False},
            {'texto': 'Um sistema que permite manipular banco de dados via código Python', 'correta': True},
            {'texto': 'Um servidor web', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual dos arquivos abaixo define as URLs em um app Django?',
        'alternativas': [
            {'texto': 'models.py', 'correta': False},
            {'texto': 'views.py', 'correta': False},
            {'texto': 'urls.py', 'correta': True},
            {'texto': 'admin.py', 'correta': False},
        ],
    },
    {
        'descricao': 'Em Django, o que a função "render" faz?',
        'alternativas': [
            {'texto': 'Envia dados para o banco de dados', 'correta': False},
            {'texto': 'Renderiza um template HTML e retorna uma resposta HTTP', 'correta': True},
            {'texto': 'Cria um modelo', 'correta': False},
            {'texto': 'Define rotas da aplicação', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual comando cria um superusuário para acessar o admin do Django?',
        'alternativas': [
            {'texto': 'python manage.py createsuperuser', 'correta': True},
            {'texto': 'python manage.py createadmin', 'correta': False},
            {'texto': 'python manage.py startuser', 'correta': False},
            {'texto': 'python manage.py runserver', 'correta': False},
        ],
    },
    {
        'descricao': 'Verdadeiro ou falso? Django fornece um painel administrativo pronto para uso.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
    }, {   'descricao': 'O que significa o comando "python manage.py migrate"?',
        'alternativas': [
            {'texto': 'Aplica migrações para criar ou atualizar o banco de dados', 'correta': True},
            {'texto': 'Cria um novo app', 'correta': False},
            {'texto': 'Roda o servidor de desenvolvimento', 'correta': False},
            {'texto': 'Cria um superusuário', 'correta': False},
        ],
    },
    {   'descricao': 'Em Django, o que é um modelo (model)?',
        'alternativas': [
            {'texto': 'Uma representação de uma tabela do banco de dados', 'correta': True},
            {'texto': 'Um arquivo HTML', 'correta': False},
            {'texto': 'Uma rota de URL', 'correta': False},
            {'texto': 'Uma classe de configuração do Django', 'correta': False},
        ],
    },
    {   'descricao': 'Qual arquivo é responsável por registrar os modelos para o painel administrativo do Django?',
        'alternativas': [
            {'texto': 'models.py', 'correta': False},
            {'texto': 'views.py', 'correta': False},
            {'texto': 'admin.py', 'correta': True},
            {'texto': 'urls.py', 'correta': False},
        ],
    },
    {   'descricao': 'Verdadeiro ou falso? O Django usa o banco de dados SQLite por padrão em novos projetos.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
    },
    {   'descricao': 'O que o comando "python manage.py startapp" faz?',
        'alternativas': [
            {'texto': 'Cria um novo app Django', 'correta': True},
            {'texto': 'Cria o banco de dados', 'correta': False},
            {'texto': 'Roda o servidor de desenvolvimento', 'correta': False},
            {'texto': 'Cria uma migração', 'correta': False},
        ],
    },
    {   'descricao': 'Qual estrutura de dados Django usa para armazenar informações do banco de dados?',
        'alternativas': [
            {'texto': 'Dictionaries', 'correta': False},
            {'texto': 'QuerySets', 'correta': True},
            {'texto': 'Tuplas', 'correta': False},
            {'texto': 'Listas', 'correta': False},
        ],
    },
    {   'descricao': 'O que a função "reverse" faz em Django?',
        'alternativas': [
            {'texto': 'Inverte a ordem de elementos em uma lista', 'correta': False},
            {'texto': 'Reverte uma URL para uma view', 'correta': True},
            {'texto': 'Realiza uma consulta no banco', 'correta': False},
            {'texto': 'Muda a ordem dos parâmetros de uma URL', 'correta': False},
        ],
    },
]

questoes_intermediario = [
    {
        'descricao': 'Qual das opções abaixo é uma maneira correta de definir um campo de texto em um modelo Django?',
        'alternativas': [
            {'texto': 'models.CharField(max_length=100)', 'correta': True},
            {'texto': 'models.TextField(max_length=100)', 'correta': False},
            {'texto': 'models.Text(max_length=100)', 'correta': False},
            {'texto': 'models.StringField(max_length=100)', 'correta': False},
        ],
    },
    {
        'descricao': 'Em Django, qual função é usada para aplicar as migrações ao banco de dados?',
        'alternativas': [
            {'texto': 'python manage.py makemigrations', 'correta': False},
            {'texto': 'python manage.py migrate', 'correta': True},
            {'texto': 'python manage.py runserver', 'correta': False},
            {'texto': 'python manage.py syncdb', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual das opções abaixo define uma relação "um-para-muitos" em modelos Django?',
        'alternativas': [
            {'texto': 'models.ManyToManyField()', 'correta': False},
            {'texto': 'models.OneToOneField()', 'correta': False},
            {'texto': 'models.ForeignKey()', 'correta': True},
            {'texto': 'models.RelatedField()', 'correta': False},
        ],
    },
    {
        'descricao': 'O que é o método "get_queryset" em uma View baseada em classe (CBV)?',
        'alternativas': [
            {'texto': 'Método que retorna o conjunto de objetos a ser exibido', 'correta': True},
            {'texto': 'Método que cria um novo objeto no banco', 'correta': False},
            {'texto': 'Método que renderiza o template', 'correta': False},
            {'texto': 'Método que trata o formulário', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual dos seguintes middlewares não é padrão do Django?',
        'alternativas': [
            {'texto': 'SecurityMiddleware', 'correta': False},
            {'texto': 'SessionMiddleware', 'correta': False},
            {'texto': 'CustomMiddleware', 'correta': True},
            {'texto': 'CommonMiddleware', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual comando cria um novo app Django?',
        'alternativas': [
            {'texto': 'django-admin startproject', 'correta': False},
            {'texto': 'python manage.py startapp', 'correta': True},
            {'texto': 'python manage.py createsuperuser', 'correta': False},
            {'texto': 'python manage.py makemigrations', 'correta': False},
        ],
    },
    {
        'descricao': 'Em Django REST Framework, qual classe é usada para criar uma ViewSet?',
        'alternativas': [
            {'texto': 'APIView', 'correta': False},
            {'texto': 'ViewSet', 'correta': True},
            {'texto': 'GenericView', 'correta': False},
            {'texto': 'Serializer', 'correta': False},
        ],
    },
    {
        'descricao': 'O que é um "QuerySet" no Django?',
        'alternativas': [
            {'texto': 'Uma coleção de objetos do banco de dados filtrados ou não', 'correta': True},
            {'texto': 'Um template HTML', 'correta': False},
            {'texto': 'Um formulário Django', 'correta': False},
            {'texto': 'Um arquivo de migração', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual o propósito do arquivo urls.py em um projeto Django?',
        'alternativas': [
            {'texto': 'Definir as rotas URL e mapear para views', 'correta': True},
            {'texto': 'Configurar banco de dados', 'correta': False},
            {'texto': 'Definir modelos', 'correta': False},
            {'texto': 'Configurar templates', 'correta': False},
        ],
    },
    {
        'descricao': 'O que é o arquivo "admin.py" em um app Django?',
        'alternativas': [
            {'texto': 'Define a interface administrativa para os modelos', 'correta': True},
            {'texto': 'Define os modelos de dados', 'correta': False},
            {'texto': 'Define as URLs', 'correta': False},
            {'texto': 'Define as views', 'correta': False},
        ],
    },{   'descricao': 'O que o Django faz ao executar "python manage.py makemigrations"?',
        'alternativas': [
            {'texto': 'Cria um arquivo de migração que descreve as alterações no modelo', 'correta': True},
            {'texto': 'Aplica migrações no banco de dados', 'correta': False},
            {'texto': 'Inicia o servidor de desenvolvimento', 'correta': False},
            {'texto': 'Cria um novo app Django', 'correta': False},
        ],
    },
    {   'descricao': 'Em Django, qual é a principal diferença entre "models.CharField" e "models.TextField"?',
        'alternativas': [
            {'texto': 'CharField é usado para textos curtos, enquanto TextField é para textos longos', 'correta': True},
            {'texto': 'CharField é para campos de data, e TextField é para números', 'correta': False},
            {'texto': 'CharField é para campos de relação entre modelos', 'correta': False},
            {'texto': 'Não há diferença entre os dois', 'correta': False},
        ],
    },
    {   'descricao': 'Em uma View baseada em função (FBV), qual método HTTP é usado para capturar dados de um formulário?',
        'alternativas': [
            {'texto': 'POST', 'correta': True},
            {'texto': 'GET', 'correta': False},
            {'texto': 'PUT', 'correta': False},
            {'texto': 'DELETE', 'correta': False},
        ],
    },
    {   'descricao': 'O que o "Django ORM" faz?',
        'alternativas': [
            {'texto': 'Permite trabalhar com o banco de dados usando Python', 'correta': True},
            {'texto': 'Permite trabalhar com arquivos JSON', 'correta': False},
            {'texto': 'Realiza renderização de templates HTML', 'correta': False},
            {'texto': 'Configura rotas de URL', 'correta': False},
        ],
    },
    {   'descricao': 'Qual a principal diferença entre "ForeignKey" e "ManyToManyField" em Django?',
        'alternativas': [
            {'texto': 'ForeignKey é uma relação de muitos para um, enquanto ManyToManyField é uma relação de muitos para muitos', 'correta': True},
            {'texto': 'ForeignKey cria um campo de texto, enquanto ManyToManyField cria uma chave primária', 'correta': False},
            {'texto': 'Não há diferença entre os dois', 'correta': False},
            {'texto': 'ForeignKey é usado apenas em views, enquanto ManyToManyField é para modelos', 'correta': False},
        ],
    },
]

questoes_avancado = [
    {
        'descricao': 'O que a função "select_related" faz em um QuerySet Django?',
        'alternativas': [
            {'texto': 'Faz um JOIN para buscar relações de forma eficiente', 'correta': True},
            {'texto': 'Seleciona somente os campos necessários', 'correta': False},
            {'texto': 'Cria uma nova relação entre modelos', 'correta': False},
            {'texto': 'Atualiza o banco de dados', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual é o propósito do middleware "CsrfViewMiddleware" em Django?',
        'alternativas': [
            {'texto': 'Proteger contra ataques CSRF (Cross Site Request Forgery)', 'correta': True},
            {'texto': 'Gerenciar sessões do usuário', 'correta': False},
            {'texto': 'Autenticar usuários', 'correta': False},
            {'texto': 'Renderizar templates', 'correta': False},
        ],
    },
    {
        'descricao': 'O que o decorador "@login_required" faz em uma view Django?',
        'alternativas': [
            {'texto': 'Exige que o usuário esteja autenticado para acessar a view', 'correta': True},
            {'texto': 'Redireciona automaticamente para a página inicial', 'correta': False},
            {'texto': 'Cria uma nova sessão para o usuário', 'correta': False},
            {'texto': 'Permite acesso público à view', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual é o efeito do método "annotate" em um QuerySet?',
        'alternativas': [
            {'texto': 'Adiciona campos calculados a cada objeto do QuerySet', 'correta': True},
            {'texto': 'Filtra o QuerySet', 'correta': False},
            {'texto': 'Ordena o QuerySet', 'correta': False},
            {'texto': 'Exclui objetos do banco', 'correta': False},
        ],
    },
    {
        'descricao': 'O que é o "Django Signals"?',
        'alternativas': [
            {'texto': 'Um mecanismo para enviar notificações entre partes do código', 'correta': True},
            {'texto': 'Um tipo de banco de dados', 'correta': False},
            {'texto': 'Um framework JavaScript', 'correta': False},
            {'texto': 'Um middleware', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual é a função do arquivo "wsgi.py" em um projeto Django?',
        'alternativas': [
            {'texto': 'Servir como ponto de entrada para servidores web compatíveis com WSGI', 'correta': True},
            {'texto': 'Configurar banco de dados', 'correta': False},
            {'texto': 'Definir modelos', 'correta': False},
            {'texto': 'Gerenciar rotas', 'correta': False},
        ],
    },
    {
        'descricao': 'Em Django REST Framework, o que faz o "Serializer"?',
        'alternativas': [
            {'texto': 'Converte objetos complexos como QuerySets para tipos nativos Python (json, xml)', 'correta': True},
            {'texto': 'Renderiza templates HTML', 'correta': False},
            {'texto': 'Gerencia URLs', 'correta': False},
            {'texto': 'Gerencia autenticação', 'correta': False},
        ],
    },
    {
        'descricao': 'Qual o propósito do método "prefetch_related"?',
        'alternativas': [
            {'texto': 'Busca relações ManyToMany e ForeignKey para evitar consultas extras', 'correta': True},
            {'texto': 'Exclui objetos relacionados', 'correta': False},
            {'texto': 'Cria índices no banco', 'correta': False},
            {'texto': 'Aplica filtros avançados', 'correta': False},
        ],
    },
    {
        'descricao': 'O que o arquivo "celery.py" normalmente configura em um projeto Django?',
        'alternativas': [
            {'texto': 'Configuração do sistema de filas para tarefas assíncronas', 'correta': True},
            {'texto': 'Configuração do banco de dados', 'correta': False},
            {'texto': 'Configuração de templates', 'correta': False},
            {'texto': 'Configuração do servidor web', 'correta': False},
        ],
    },
    {
        'descricao': 'O que é um "Custom Manager" em Django?',
        'alternativas': [
            {'texto': 'Uma classe para definir consultas personalizadas no ORM', 'correta': True},
            {'texto': 'Um tipo especial de view', 'correta': False},
            {'texto': 'Um template customizado', 'correta': False},
            {'texto': 'Um middleware', 'correta': False},
        ],
    },{   'descricao': 'O que é o "Django Signals" e como ele pode ser utilizado em projetos Django?',
        'alternativas': [
            {'texto': 'É um sistema para enviar notificações e permitir que componentes desacoplados respondam a eventos', 'correta': True},
            {'texto': 'É um sistema de cache para melhorar o desempenho', 'correta': False},
            {'texto': 'É uma ferramenta para autenticação de usuários', 'correta': False},
            {'texto': 'É um módulo para realizar backup do banco de dados', 'correta': False},
        ],
    },
    {   'descricao': 'Qual a principal diferença entre o uso de "prefetch_related" e "select_related" no Django ORM?',
        'alternativas': [
            {'texto': 'select_related é usado para relações ForeignKey e OneToOne, enquanto prefetch_related é para ManyToMany e reverse ForeignKey', 'correta': True},
            {'texto': 'select_related é mais eficiente, enquanto prefetch_related pode gerar consultas desnecessárias', 'correta': False},
            {'texto': 'prefetch_related é usado apenas em consultas com filtros, e select_related sem filtros', 'correta': False},
            {'texto': 'Não há diferença entre os dois, eles fazem a mesma coisa', 'correta': False},
        ],
    },
    {   'descricao': 'Quando usar o método "annotate" em um QuerySet do Django?',
        'alternativas': [
            {'texto': 'Quando você precisa adicionar informações agregadas (como soma ou contagem) a cada objeto retornado no QuerySet', 'correta': True},
            {'texto': 'Quando você quer modificar os dados do banco diretamente', 'correta': False},
            {'texto': 'Quando você precisa filtrar os resultados', 'correta': False},
            {'texto': 'Quando você precisa ordenar os resultados', 'correta': False},
        ],
    },
    {   'descricao': 'O que o arquivo "wsgi.py" faz em um projeto Django?',
        'alternativas': [
            {'texto': 'Define o ponto de entrada para servidores web que utilizam o protocolo WSGI', 'correta': True},
            {'texto': 'Define as rotas de URL do projeto', 'correta': False},
            {'texto': 'Configura os modelos de dados do projeto', 'correta': False},
            {'texto': 'Configura as migrações do banco de dados', 'correta': False},
        ],
    },
    {   'descricao': 'Como você pode melhorar a performance de consultas em Django quando estiver lidando com grandes volumes de dados?',
        'alternativas': [
            {'texto': 'Usando select_related e prefetch_related para otimizar as consultas e reduzir o número de queries ao banco de dados', 'correta': True},
            {'texto': 'Usando o método "all()" em todos os modelos', 'correta': False},
            {'texto': 'Desativando o uso de indexes no banco de dados', 'correta': False},
            {'texto': 'Executando consultas SQL diretamente no banco de dados sem passar pelo ORM', 'correta': False},
        ],
    },
]

# Função para popular questões em cada quiz
def popular_questoes(quiz, questoes):
    for q in questoes:
        questao, q_created = Questao.objects.get_or_create(quiz=quiz, descricao=q['descricao'])
        if not q_created:
            for alt in q['alternativas']:
                alternativa, a_created = Alternativa.objects.get_or_create(questao=questao, texto=alt['texto'])
                if not a_created:
                    if alt['correta']:
                        Resposta.objects.create(questao=questao, alternativa=alternativa, explicacao="")

# Popular os quizzes
popular_questoes(quiz_iniciante, questoes_iniciante)
popular_questoes(quiz_intermediario, questoes_intermediario)
popular_questoes(quiz_avancado, questoes_avancado)

# Cria o usuário se não existir
usuario, created = User.objects.get_or_create(username="palermo")
if created:
    usuario.set_password("palermo123")
    usuario.save()

# Cria o certificado para o usuário
certificado, created = Certificado.objects.get_or_create(
    codigo="CERT12345",
    usuario=usuario,
    disciplina=disciplina
)
