from flask import Flask, redirect, url_for, render_template, request, session
from spotifyWebBackend import PlaylistCreation
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from SpotifySecret import client_id, client_secret, redirect_uri

app = Flask(__name__)
app.secret_key = #hidden



@app.route("/login", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        if "token" in session:
            playlistName = request.form["playlistName"]
            vibe = int(request.form["vibe"])
            playlist_name = request.form["newPlaylistName"]
            playlistCreation = PlaylistCreation()
            token = session["token"]
            #playlists = session["playlists"]
            playlistCreation.mainMethod(playlistName, vibe, playlist_name, token)
            return redirect(url_for("user", usr=playlist_name))
        else:
            return redirect(url_for("/"))
    else:
        scope = ' '.join([
            'user-read-email',
            'playlist-read-private',
            'playlist-modify-private',
            'playlist-modify-public',
        ])
        code = request.args.get('code')


        auth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
        token = auth.get_access_token(code)['access_token']
        session["token"] = token
        getImage = PlaylistCreation()
        url = getImage.getPlaylistImage(token)

        return render_template("getPostAttempt.html", url1=url[0][0][0]['url'], playlistName1= url[0][1], songsNum1=url[0][2], url2=url[1][0][0]['url'], playlistName2= url[1][1], songsNum2=url[1][2], url3=url[2][0][0]['url'], playlistName3= url[2][1], songsNum3=url[2][2])

@app.route("/<usr>")
def user(usr):
    if "token" in session:
        session.pop("user", None)
    return f"<h1>Congratulations {usr} has been created</h1>"

@app.route("/")
def login():
    return render_template("SpotifyCreate Page.html")

if __name__ == '__main__':
    app.run()

