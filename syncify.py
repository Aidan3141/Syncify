import os
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
app = Flask(__name__)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

# Initializing spotify's OAuth (for login)
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read",
    cache_path=".cache"
)

sp = spotipy.Spotify(auth_manager=auth_manager)

#"fake" user data to compare to actual user's listening history
fake_user_data = {
    "top_artists": ["beabadoobee", "The Weeknd", "keshi", "Billie Eilish", "Gracie Abrams"],
    "top_tracks": ["Everything I Want", "Shake It Off", "Rolling in the Deep", "Happier Than Ever", "One Dance"]
}

#home
@app.route('/')
def index():
    return render_template('index.html')


#using spotipy to get user's top artists & tracks
@app.route('/api/top')
def get_top_data():
    try:
        #getting logged-in user's top artist
        top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
        user_top_artists = [artist['name'] for artist in top_artists['items']]

        #getting logged-in user's top track
        top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
        user_top_tracks = [track['name'] for track in top_tracks['items']]

        #returning both with jsonify to return as an http response
        return jsonify({"user_top_artists": user_top_artists,"user_top_tracks": user_top_tracks})
    #if there's an error, save it and print it on page
    except Exception as e:
        return jsonify({"error": str(e)})

#based upon spotipy's fetched user data, compare to "fake" data
@app.route('/api/compare')
def compare_data():
    try:
        #getting logged-in user's top artists and tracks
        top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
        user_top_artists = {artist['name'] for artist in top_artists['items']}

        top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
        user_top_tracks = {track['name'] for track in top_tracks['items']}

        #fake user's data
        fake_top_artists = set(fake_user_data["top_artists"])
        fake_top_tracks = set(fake_user_data["top_tracks"])

        #calculating similarity as a percentage
        artist_similarity = len(user_top_artists & fake_top_artists) / len(user_top_artists | fake_top_artists) * 100
        track_similarity = len(user_top_tracks & fake_top_tracks) / len(user_top_tracks | fake_top_tracks) * 100

        #returning data rounding to 2 decimals
        return jsonify({
            "artist_similarity": round(artist_similarity, 2),
            "track_similarity": round(track_similarity, 2),
            "fake_user_data": fake_user_data
        })
    #if there's an error, save it and print it on page
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
