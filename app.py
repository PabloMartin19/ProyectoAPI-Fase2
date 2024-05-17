from flask import Flask, render_template, request, flash
import requests

# Importar la función get_access_token desde KEY.py
from KEY import get_access_token
from flash_key import generate_secret_key

app = Flask(__name__)
app.secret_key = generate_secret_key()

def search_artists(query):
    token = get_access_token()
    url = f'https://api.spotify.com/v1/search?q={query}&type=artist'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()['artists']['items']

def get_artist_info(artist_id):
    token = get_access_token()
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_artist_albums(artist_id):
    token = get_access_token()
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()['items']

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
    app.run(debug=True)
