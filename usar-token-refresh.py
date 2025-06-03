from datetime import datetime
import time
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
        print("Failed to obtain token:", response.text)
        return None

def refresh_token(refresh):
    response = requests.post(API_URL + 'token/refresh/', data={
        'refresh': refresh,
    })
    if response.status_code == 200:
        print("Token atualizado com sucesso:", response.json())
        return response.json()
    else:
        print("Failed to refresh token:", response.text)
        return None

def my_profile(access):
    response = requests.get(API_URL + 'profile/', headers={'Authorization': f'Bearer {access}'})
    if response.status_code == 200:
        print("Perfil do usuário:", response.json()['message'])
        return True
    else:
        print("Token expirado ou inválido:", response.text)
        return False

if __name__ == "__main__":
    token = get_token()
    if not token:
        exit(1)

    for i in range(30):
        time.sleep(1)
        now = datetime.now()
        print(f'{now.hour:02}:{now.minute:02}:{now.second:02} - Testando acesso ao perfil...')

        if not my_profile(token['access']):
            print("Tentando atualizar token...")
            token_refresh = refresh_token(token['refresh'])
            if token_refresh and 'access' in token_refresh:
                token['access'] = token_refresh['access']
                print("Novo access token obtido!")
            else:
                print("Não foi possível atualizar o token. Encerrando.")
                break