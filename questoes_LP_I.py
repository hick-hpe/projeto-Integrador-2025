from devquiz.api.models import *
from django.contrib.auth.models import User

# Busca ou cria a disciplina
disciplina, _ = Disciplina.objects.get_or_create(nome='Linguagem de programação I')

# Apaga todas as questões existentes para evitar duplicação
for q in Questao.objects.all():
    q.delete()

# Cria os 3 quizzes por nível
quiz_iniciante, _ = Quiz.objects.get_or_create(disciplina=disciplina, nivel="Iniciante")
quiz_intermediario, _ = Quiz.objects.get_or_create(disciplina=disciplina, nivel="Intermediário")
quiz_avancado, _ = Quiz.objects.get_or_create(disciplina=disciplina, nivel="Avançado")

# Questões para cada nível (10 de cada nível)
questoes_iniciante = [
    {
        'descricao': 'O que é uma variável em Java?',
        'alternativas': [
            {'texto': 'Um espaço na memória para armazenar valores.', 'correta': True},
            {'texto': 'Um comando de repetição.', 'correta': False},
            {'texto': 'Uma função que retorna valores.', 'correta': False},
            {'texto': 'Um tipo de dado booleano.', 'correta': False},
        ],
        'explicacao': 'Variáveis armazenam valores temporários na memória para uso durante a execução do programa.',
    },
    {
        'descricao': 'Qual é o comando para imprimir algo na tela em Java?',
        'alternativas': [
            {'texto': 'System.out.println();', 'correta': True},
            {'texto': 'print();', 'correta': False},
            {'texto': 'echo();', 'correta': False},
            {'texto': 'Console.WriteLine();', 'correta': False},
        ],
        'explicacao': 'System.out.println() é o comando padrão para saída no console em Java.',
    },
    {
        'descricao': 'Verdadeiro ou falso: Em Java, toda instrução deve terminar com ponto e vírgula.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'Em Java, todas as instruções (comandos) terminam com ponto e vírgula.',
    },
    {
        'descricao': 'Qual destas opções representa um tipo primitivo em Java?',
        'alternativas': [
            {'texto': 'int', 'correta': True},
            {'texto': 'String', 'correta': False},
            {'texto': 'Scanner', 'correta': False},
            {'texto': 'System', 'correta': False},
        ],
        'explicacao': 'int é um tipo primitivo; String, Scanner e System são classes.',
    },
    {
        'descricao': 'Como se declara um array de inteiros em Java?',
        'alternativas': [
            {'texto': 'int[] numeros;', 'correta': True},
            {'texto': 'array int numeros;', 'correta': False},
            {'texto': 'int numeros[];', 'correta': True},
            {'texto': 'numeros = int[];', 'correta': False},
        ],
        'explicacao': 'int[] numeros; ou int numeros[]; são formas válidas, mas a mais comum é int[] numeros;',
    },
    {
        'descricao': 'O que faz o operador == em Java?',
        'alternativas': [
            {'texto': 'Compara se dois valores são iguais.', 'correta': True},
            {'texto': 'Atribui um valor a uma variável.', 'correta': False},
            {'texto': 'Compara se dois valores são diferentes.', 'correta': False},
            {'texto': 'Incrementa o valor de uma variável.', 'correta': False},
        ],
        'explicacao': 'O operador == compara igualdade entre valores primitivos.',
    },
    {
        'descricao': 'Qual destas estruturas é usada para repetição em Java?',
        'alternativas': [
            {'texto': 'for', 'correta': True},
            {'texto': 'if', 'correta': False},
            {'texto': 'switch', 'correta': False},
            {'texto': 'case', 'correta': False},
        ],
        'explicacao': 'A estrutura for é usada para laços de repetição.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O método main é o ponto de entrada de um programa Java.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'O método main é onde a execução do programa Java começa.',
    },
    {
        'descricao': 'Qual palavra-chave é usada para criar um novo objeto em Java?',
        'alternativas': [
            {'texto': 'new', 'correta': True},
            {'texto': 'create', 'correta': False},
            {'texto': 'object', 'correta': False},
            {'texto': 'instance', 'correta': False},
        ],
        'explicacao': 'A palavra-chave new é usada para instanciar objetos.',
    },
    {
        'descricao': 'O que significa POO?',
        'alternativas': [
            {'texto': 'Programação Orientada a Objetos', 'correta': True},
            {'texto': 'Programa Operacional de Objetos', 'correta': False},
            {'texto': 'Processo de Organização de Objetos', 'correta': False},
            {'texto': 'Programa de Operação de Objetos', 'correta': False},
        ],
        'explicacao': 'POO significa Programação Orientada a Objetos.',
    },
    {
        'descricao': 'Qual destas opções é um exemplo de laço while em Java?',
        'alternativas': [
            {'texto': 'while (condicao) { /* código */ }', 'correta': True},
            {'texto': 'repeat { /* código */ } until (condicao);', 'correta': False},
            {'texto': 'do { /* código */ }', 'correta': False},
            {'texto': 'loop (condicao) { /* código */ }', 'correta': False},
        ],
        'explicacao': 'A sintaxe correta do laço while em Java é while (condicao) { ... }',
    },
    {
        'descricao': 'Verdadeiro ou falso: Java diferencia letras maiúsculas de minúsculas.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'Java é case sensitive, ou seja, diferencia maiúsculas de minúsculas.',
    },
    {
        'descricao': 'Qual destas opções é um comentário de linha única em Java?',
        'alternativas': [
            {'texto': '// comentário', 'correta': True},
            {'texto': '/* comentário */', 'correta': False},
            {'texto': '<!-- comentário -->', 'correta': False},
            {'texto': '# comentário', 'correta': False},
        ],
        'explicacao': '// é usado para comentários de linha única em Java.',
    },
    {
        'descricao': 'O que faz o comando break em um laço?',
        'alternativas': [
            {'texto': 'Interrompe a execução do laço.', 'correta': True},
            {'texto': 'Continua para a próxima iteração.', 'correta': False},
            {'texto': 'Reinicia o laço.', 'correta': False},
            {'texto': 'Ignora a condição do laço.', 'correta': False},
        ],
        'explicacao': 'break encerra imediatamente o laço onde está inserido.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O comando continue pula para a próxima iteração do laço.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'continue faz o laço pular para a próxima iteração.',
    },
]

questoes_intermediario = [
    {
        'descricao': 'Qual é a saída do código: int x = 5; System.out.println(x++);',
        'alternativas': [
            {'texto': '5', 'correta': True},
            {'texto': '6', 'correta': False},
            {'texto': 'Erro de compilação', 'correta': False},
            {'texto': '0', 'correta': False},
        ],
        'explicacao': 'O operador x++ retorna o valor antes de incrementar, então imprime 5.',
    },
    {
        'descricao': 'Qual destas opções representa corretamente um método em Java?',
        'alternativas': [
            {'texto': 'public int soma(int a, int b) { return a + b; }', 'correta': True},
            {'texto': 'function soma(a, b) { return a + b; }', 'correta': False},
            {'texto': 'def soma(a, b): return a + b', 'correta': False},
            {'texto': 'soma = (a, b) -> a + b', 'correta': False},
        ],
        'explicacao': 'A sintaxe correta de método em Java é: public int soma(int a, int b) { ... }',
    },
    {
        'descricao': 'Verdadeiro ou falso: O método equals() compara o conteúdo de objetos em Java.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'equals() compara o conteúdo; == compara referências.',
    },
    {
        'descricao': 'Qual destas opções ordena corretamente um array em ordem crescente usando bubble sort?',
        'alternativas': [
            {'texto': 'Comparar elementos adjacentes e trocar se estiverem fora de ordem, repetindo até o final.', 'correta': True},
            {'texto': 'Dividir o array ao meio e ordenar cada parte.', 'correta': False},
            {'texto': 'Escolher um pivô e particionar o array.', 'correta': False},
            {'texto': 'Inserir cada elemento na posição correta.', 'correta': False},
        ],
        'explicacao': 'Bubble sort compara e troca elementos adjacentes até o array estar ordenado.',
    },
    {
        'descricao': 'O que é encapsulamento em POO?',
        'alternativas': [
            {'texto': 'Proteger os dados de um objeto, permitindo acesso apenas por métodos.', 'correta': True},
            {'texto': 'Permitir que uma classe herde de outra.', 'correta': False},
            {'texto': 'Permitir múltiplas implementações de um método.', 'correta': False},
            {'texto': 'Dividir o código em funções pequenas.', 'correta': False},
        ],
        'explicacao': 'Encapsulamento restringe o acesso direto aos atributos, usando métodos para manipulação.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O algoritmo de seleção (selection sort) sempre faz o mesmo número de comparações, independentemente da entrada.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'Selection sort sempre faz n(n-1)/2 comparações, independentemente da ordem inicial.',
    },
    {
        'descricao': 'Qual palavra-chave é usada para herança em Java?',
        'alternativas': [
            {'texto': 'extends', 'correta': True},
            {'texto': 'inherits', 'correta': False},
            {'texto': 'super', 'correta': False},
            {'texto': 'base', 'correta': False},
        ],
        'explicacao': 'A palavra-chave extends indica herança em Java.',
    },
    {
        'descricao': 'O que faz o método toString() em uma classe Java?',
        'alternativas': [
            {'texto': 'Retorna uma representação em texto do objeto.', 'correta': True},
            {'texto': 'Converte o objeto em inteiro.', 'correta': False},
            {'texto': 'Compara dois objetos.', 'correta': False},
            {'texto': 'Cria uma cópia do objeto.', 'correta': False},
        ],
        'explicacao': 'toString() retorna uma string representando o objeto.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O algoritmo insertion sort é eficiente para listas pequenas.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'Insertion sort é eficiente para listas pequenas ou quase ordenadas.',
    },
    {
        'descricao': 'Qual destas opções representa polimorfismo?',
        'alternativas': [
            {'texto': 'Um método com o mesmo nome, mas comportamentos diferentes em subclasses.', 'correta': True},
            {'texto': 'Acesso direto aos atributos de uma classe.', 'correta': False},
            {'texto': 'Uso de variáveis globais.', 'correta': False},
            {'texto': 'Divisão do código em funções pequenas.', 'correta': False},
        ],
        'explicacao': 'Polimorfismo permite que métodos com o mesmo nome tenham comportamentos diferentes em subclasses.',
    },
    {
        'descricao': 'O que é um construtor em Java?',
        'alternativas': [
            {'texto': 'Um método especial chamado ao criar um objeto.', 'correta': True},
            {'texto': 'Um método que destrói objetos.', 'correta': False},
            {'texto': 'Um método estático.', 'correta': False},
            {'texto': 'Um atributo da classe.', 'correta': False},
        ],
        'explicacao': 'Construtores inicializam objetos e têm o mesmo nome da classe.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O método compareTo() é usado para comparar objetos em ordenação.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'compareTo() é usado para comparar objetos, especialmente em ordenações.',
    },
]

questoes_avancado = [
    {
        'descricao': 'Qual é a complexidade de tempo média do algoritmo quicksort?',
        'alternativas': [
            {'texto': 'O(n log n)', 'correta': True},
            {'texto': 'O(n^2)', 'correta': False},
            {'texto': 'O(n)', 'correta': False},
            {'texto': 'O(log n)', 'correta': False},
        ],
        'explicacao': 'A complexidade média do quicksort é O(n log n).',
    },
    {
        'descricao': 'Verdadeiro ou falso: O método equals() pode ser sobrescrito em uma classe Java.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'O método equals() pode ser sobrescrito para definir igualdade personalizada.',
    },
    {
        'descricao': 'Qual destas opções representa corretamente a sobrescrita de método em Java?',
        'alternativas': [
            {'texto': 'Usar @Override antes do método na subclasse.', 'correta': True},
            {'texto': 'Usar @Overload antes do método.', 'correta': False},
            {'texto': 'Declarar o método como static.', 'correta': False},
            {'texto': 'Declarar o método como final.', 'correta': False},
        ],
        'explicacao': 'A anotação @Override indica sobrescrita de método.',
    },
    {
        'descricao': 'O que é recursão?',
        'alternativas': [
            {'texto': 'Quando um método chama a si mesmo.', 'correta': True},
            {'texto': 'Quando um método chama outro método.', 'correta': False},
            {'texto': 'Quando um método é chamado apenas uma vez.', 'correta': False},
            {'texto': 'Quando um método é privado.', 'correta': False},
        ],
        'explicacao': 'Recursão ocorre quando um método chama a si mesmo.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O algoritmo merge sort é estável.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'Merge sort é um algoritmo de ordenação estável.',
    },
    {
        'descricao': 'Qual destas opções representa corretamente a implementação de uma interface?',
        'alternativas': [
            {'texto': 'public class Exemplo implements MinhaInterface { ... }', 'correta': True},
            {'texto': 'public class Exemplo extends MinhaInterface { ... }', 'correta': False},
            {'texto': 'public interface Exemplo implements MinhaInterface { ... }', 'correta': False},
            {'texto': 'public class Exemplo interface MinhaInterface { ... }', 'correta': False},
        ],
        'explicacao': 'Usamos a palavra-chave implements para implementar uma interface em Java.',
    },
    {
        'descricao': 'O que é o padrão de projeto Singleton?',
        'alternativas': [
            {'texto': 'Garante que uma classe tenha apenas uma instância e forneça um ponto global de acesso a ela.', 'correta': True},
            {'texto': 'Permite que uma classe tenha múltiplas instâncias.', 'correta': False},
            {'texto': 'Define uma interface para criar famílias de objetos relacionados.', 'correta': False},
            {'texto': 'Cria objetos em tempo de execução.', 'correta': False},
        ],
        'explicacao': 'O padrão Singleton garante que uma classe tenha apenas uma instância durante toda a execução do programa.',
    },
    {
        'descricao': 'Verdadeiro ou falso: O padrão de projeto Factory Method é utilizado para criar objetos sem especificar a classe exata.',
        'alternativas': [
            {'texto': 'Verdadeiro', 'correta': True},
            {'texto': 'Falso', 'correta': False},
        ],
        'explicacao': 'O Factory Method permite criar objetos sem especificar a classe exata, delegando essa responsabilidade a subclasses.',
    },
]

# Função para popular questões em cada quiz
def popular_questoes(quiz, questoes):
    for q in questoes:
        questao = Questao.objects.create(quiz=quiz, descricao=q['descricao'])
        for alt in q['alternativas']:
            alternativa = Alternativa.objects.create(questao=questao, texto=alt['texto'])
            if alt['correta']:
                Resposta.objects.create(questao=questao, alternativa=alternativa, explicacao=q['explicacao'])

# Popular os quizzes
popular_questoes(quiz_iniciante, questoes_iniciante)
popular_questoes(quiz_intermediario, questoes_intermediario)
popular_questoes(quiz_avancado, questoes_avancado)


