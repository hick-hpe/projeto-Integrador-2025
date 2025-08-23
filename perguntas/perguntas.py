import json

perguntas = []

def carregar_perguntas(caminho_arquivo):
    global perguntas
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        perguntas = json.load(arquivo)
        perguntas = perguntas['niveis']
    return perguntas

# numero total de perguntas
def total_perguntas():
    soma = 0
    for nivel in perguntas:
        if nivel in ['iniciante', 'intermediario']:
            soma += len(perguntas[nivel])
    return soma

if __name__ == "__main__":
    caminho_arquivo = 'perguntas.json'
    caminho_novo_arquivo = 'perguntas_niveladas.json'

    niveis = ['iniciante', 'intermediario']
    carregar_perguntas(caminho_arquivo)

    print(f'Total de perguntas: {total_perguntas()}')

    # dividir perguntas dos 2 níveis para 3 níveis
    perguntas_niveladas = {}

    # iniciante: 10 primeiras
    # intermediario: pegar as 5 ultimas do iniciante + 5 primeiras do intermediario
    # avancado: pegar as 10 ultimas do intermediario
    perguntas_niveladas['iniciante'] = perguntas['iniciante'][:10]
    perguntas_niveladas['intermediario'] = perguntas['iniciante'][10:] + perguntas['intermediario'][:5]
    perguntas_niveladas['avancado'] = perguntas['intermediario'][5:15]

    # contar cada nivel de pergunta pra verificar se a divisão está correta: 10 para cada nível
    for nivel, perguntas_nivel in perguntas_niveladas.items():
        print(f'Perguntas nível {nivel}: {len(perguntas_nivel)}')

    # salvar novo arquivo
    with open(caminho_novo_arquivo, 'w', encoding='utf-8') as novo_arquivo:
        json.dump(perguntas_niveladas, novo_arquivo, ensure_ascii=False, indent=4)

