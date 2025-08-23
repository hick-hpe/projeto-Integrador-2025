import json

perguntas = []

def carregar_perguntas(caminho_arquivo, nivel):
    global perguntas
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        perguntas = json.load(arquivo)
        perguntas = perguntas[nivel]
    return perguntas

def exibir_perguntas(caminho_arquivo, nivel):
    perguntas_nivel = carregar_perguntas(caminho_arquivo, nivel)
    for i, pergunta in enumerate(perguntas_nivel, start=1):
        print(f"{i:02}: {pergunta['descricao']}")
        for alternativa in pergunta['alternativas']:
            if alternativa == pergunta['resposta']:
                print(f"-> {alternativa} (Resposta Correta)")
            else:
                print(f"- {alternativa}")
        print(f"Resposta correta: {pergunta['resposta']}")
        print(f"Explicação: {pergunta['explicacao']}\n")

if __name__ == "__main__":
    caminho_arquivo = 'perguntas_niveladas.json'
    nivel = input("Digite o nível de perguntas (iniciante, intermediario, avancado): ").strip().lower()
    
    if nivel not in ['iniciante', 'intermediario', 'avancado']:
        print("Nível inválido. Por favor, escolha entre iniciante, intermediario ou avancado.")
    else:
        exibir_perguntas(caminho_arquivo, nivel)
