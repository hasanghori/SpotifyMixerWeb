from flask import Flask, redirect, url_for, render_template, request
from spotifyWebBackend import PlaylistCreation

app = Flask(__name__)

"""@app.route("/")
def home():
    return render_template("SpotifyCreate Page.html")"""


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        playlistName = request.form["playlistName"]
        vibe = int(request.form["vibe"])
        playlist_name = request.form["newPlaylistName"]
        playlistCreation = PlaylistCreation()
        playlistCreation.mainMethod(playlistName, vibe, playlist_name)
        return redirect(url_for("user", usr=playlist_name))
    else:
        return render_template("getPostAttempt.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>Congratulations {usr} has been created</h1>"

@app.route("/login")
def admin():
    return redirect("https://accounts.spotify.com/authorize?client_id=0564e53d485643aaa292796e7d73cc43&response_type=code&redirect_uri=http%3A%2F%2Fspotifyunlocked.pythonanywhere.com&scope=user-read-email%20playlist-read-private%20playlist-modify-private%20playlist-modify-public") # redirects you through to the name function
#https://accounts.spotify.com/authorize?client_id=0564e53d485643aaa292796e7d73cc43&response_type=code&redirect_uri=http%3A%2F%2Fspotifypro.pythonanywhere.com&scope=user-read-email%20playlist-read-private%20playlist-modify-private%20playlist-modify-public

if __name__ == '__main__':
    app.run()

