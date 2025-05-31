import requests

API_URL = 'http://127.0.0.1:8000/api/quizzes/3/questoes/'

def responder_quiz():
    questoes = requests.get(API_URL).json()
    
    for idx, questao in enumerate(questoes, start=1):
        print(f"\nQuestão {idx}/{len(questoes)}: {questao['descricao']}")
        alternativas = questao['alternativas']
        for i, alternativa in enumerate(alternativas, start=1):
            print(f"{i}. {alternativa['texto']}")

        while True:
            try:
                resposta = int(input("Digite o número da alternativa correta: "))
                alternativa_id = alternativas[resposta-1]['id']
                break
            except (ValueError, IndexError):
                print("Opção inválida. Tente novamente.")
        
        # Enviar resposta
        resposta_data = {
            'alternativa_id': alternativa_id
        }
        response = requests.post(API_URL + str(questao['id']) + '/', json=resposta_data)
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"Resultado: {resultado['msg']}")
            if 'explicacao' in resultado:
                print(f"Explicação: {resultado['explicacao']}")
        else:
            print("Erro ao enviar resposta.")

if __name__ == "__main__":
    responder_quiz()