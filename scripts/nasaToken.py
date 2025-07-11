import requests
import base64
import datetime

# Settings
USERNAME = "willianfloresac"
PASSWORD = "&5H!eIRq#&3uZj0V"
API_BASE_URL = "https://urs.earthdata.nasa.gov/api/users"
HEADERS = {
    "Authorization": f"Basic {base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()}"
}

def listTokens():
    """Lista tokens existentes do usuário."""
    response = requests.get(f"{API_BASE_URL}/tokens", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao listar tokens: {response.status_code} - {response.text}")
        return None

def revokeToken(token):
    """Revoga um token existente."""
    response = requests.post(
        f"{API_BASE_URL}/revoke_token?token={token}", headers=HEADERS
    )
    if response.status_code == 200:
        print("Token revogado com sucesso.")
    else:
        print(f"Erro ao revogar token: {response.status_code} - {response.text}")


def createToken():
    """Cria um novo token e salva em um arquivo."""
    response = requests.post(f"{API_BASE_URL}/token", headers=HEADERS)
    if response.status_code == 200:
        token_data = response.json()
        print("Novo token gerado:", token_data)
        # Save the token in a file
        with open("/home/srvadmin/nokekoiApp/datasets/suomi-npp-viirs-c2/token/token.txt", "w") as file:
            file.write(token_data["access_token"])
        return token_data
    else:
        print(f"Erro ao criar token: {response.status_code} - {response.text}")
        return None

def checkAndRenewTokens():
    """Verifica tokens e renova se necessário."""
    tokens = listTokens()
    if tokens is None:
        return

    if len(tokens) >= 2:
        print("Máximo de tokens atingido. Revogando o mais antigo...")
        # Order tokens by the expiration date
        tokens.sort(key=lambda x: datetime.datetime.strptime(x["expiration_date"], "%m/%d/%Y"))
        revokeToken(tokens[0]["access_token"])

    print("Criando novo token...")
    new_token = createToken()
    if new_token:
        print("Token salvo em arquivo.")

# Renewal scheduling
if __name__ == "__main__":
    checkAndRenewTokens()
