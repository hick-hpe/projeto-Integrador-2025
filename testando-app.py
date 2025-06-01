import requests

API_URL = 'http://localhost:8000/auth/'
token = {}

def get_token():
    response = requests.post(API_URL + 'token/', data={
        'username': 'Henrique',
        'password': 'henrique123',
    })
    
    if response.status_code == 200:
        print("Token obtido com sucesso:", response.json())
        return response.json()
    else:
        print("Failed to obtain token:", response.json())
        return None


def refresh_token():
    if not token:
        print("No token available to refresh.")
        return None
    
    response = requests.post(API_URL + 'token/refresh/', data={
        'refresh': token.get('refresh', '') if isinstance(token, dict) else ''
    })
    
    if response.status_code == 200:
        print("Token atualizado com sucesso:", response.json())
        return response.json()
    else:
        print("Failed to refresh token:", response.json())
        return None


def main():
    global token
    while True:
        opcao = int(input("Escolha uma opção:\n1. Obter Token\n2. Atualizar Token\n3. Ver Perfil\n4. Sair\nOpção: "))
        if opcao == 1:
            token = get_token()
        elif opcao == 2:
            token = refresh_token()
        elif opcao == 3:
            if not token or 'access' not in token:
                print("Você precisa obter um token primeiro.")
                continue
            response = requests.get(API_URL + 'profile/', headers={'Authorization': f"Bearer {token['access']}"})
            print("Resposta:", response.status_code, response.text)
        elif opcao == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()