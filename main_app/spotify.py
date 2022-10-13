import requests
import environ

env = environ.Env()

spotify_client_id = env('SPOTIFY_CLIENTID')
spotify_secret = env('SPOTIFY_CLIENT_SECRET')

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': spotify_client_id,
    'client_secret': spotify_secret,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'

# track_id = '6y0igZArWVi6Iz0rj35c1Y'
# artist_id = '3dz0NnIZhtKKeXZxLOxCam'
# artist_id = '7FBcuc1gsnv6Y1nwFtNRCb'
# track_id = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
# artist_top_songs = requests.get(BASE_URL + 'artists/' + artist_id + '/top-tracks' +'?market=US', headers=headers)
	# https://api.spotify.com/v1/artists/{id}/top-tracks

# track_id = track_id.json()

# artist_top_songs = artist_top_songs.json()


def artist_topsongs(artist_id):
    artist_top_songs = requests.get(BASE_URL + 'artists/' + artist_id + '/top-tracks' +'?market=US', headers=headers)
    artist_top_songs = artist_top_songs.json()
    return artist_top_songs

# https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb/top-tracks

def artist_related_artists(artist_id):
    related_artists = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists', headers=headers)
    related_artists = related_artists.json()
    return related_artists

