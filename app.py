from flask import Flask, render_template, request, flash
import requests
import os
from requests.auth import HTTPBasicAuth

def get_access_token():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not client_id or not client_secret:
        print("Las credenciales no están disponibles")
        return None
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    if response.status_code != 200:
        print(f"Error en la petición: {response.status_code}")
        print(response.json())
        return None
    response_data = response.json()
    access_token = response_data.get('access_token')
    return access_token

def search_artists(query):
    token = get_access_token()
    if not token:
        return []
    url = f'https://api.spotify.com/v1/search?q={query}&type=artist'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error en la búsqueda de artistas: {response.json()}")
        return []
    return response.json()['artists']['items']

def get_artist_info(artist_id):
    token = get_access_token()
    if not token:
        return {}
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error obteniendo información del artista: {response.json()}")
        return {}
    return response.json()

def get_artist_albums(artist_id):
    token = get_access_token()
    if not token:
        return []
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error obteniendo álbumes del artista: {response.json()}")
        return []
    return response.json()['items']

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()
    if not query:
        flash('Please enter an artist name to search.')
        return render_template('index.html')
    
    artists = search_artists(query)
    return render_template('search_results.html', artists=artists)

@app.route('/artist/<artist_id>')
def artist_detail(artist_id):
    artist = get_artist_info(artist_id)
    albums = get_artist_albums(artist_id)
    return render_template('artist_detail.html', artist=artist, albums=albums)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
