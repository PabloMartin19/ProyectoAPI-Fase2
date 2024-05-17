# Programa para devolver el acces_token

import requests
import base64

def get_access_token():
    client_id = '8027f29a08224610a5a30ff41ad028a1'
    client_secret = '5c380b9b4a3e48349ec1b13cb1e40a29'

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.json()}")
        return None

if __name__ == "__main__":
    token = get_access_token()
    if token:
        print(f"Access Token: {token}")