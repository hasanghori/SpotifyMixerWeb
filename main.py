from flask import Flask, redirect, url_for, render_template, request, session
from spotifyWebBackend import PlaylistCreation
from datetime import timedelta
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from SpotifySecret import client_id, client_secret, redirect_uri
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "PLZWORK"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="SpotifyUnlocked",
    password="SacKings2020",
    hostname="SpotifyUnlocked.mysql.pythonanywhere-services.com",
    databasename="SpotifyUnlocked$vibes",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    mood = db.relationship('Mood', backref='author', lazy=True)
    

    def __repr__(self):
        return f"users('{self.username}')"

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vibeName = db.Column(db.String(20))
    acousticness = db.Column(db.Integer)
    danceability = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    tempo = db.Column(db.Integer)
    valence = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, vibeName, acousticness, danceability, energy, tempo, valence, user_id):
        self.vibeName = vibeName
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.tempo = tempo
        self.valence = valence
        self.user_id = user_id

    def __repr__(self):
        return f"Vibe('{self.vibeName}','{self.acousticness}', '{self.danceability}', '{self.energy}', '{self.tempo}', '{self.valence}')"

"""class MusicProfile(db.Model):
    id = db.Column()
    user_id = db.Column("user_id", )
    user = db.relationship(User, backref="music_profile")"""
"""@app.route("/")
def home():
    return render_template("Spot`ifyCreate Page.html")"""

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
        # lookup code query parameter from request
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

        #session["playlists"] = getImage.loadPlaylists(token=token)

        return render_template("getPostAttempt.html", url1=url[0][0][0]['url'], playlistName1= url[0][1], songsNum1=url[0][2], url2=url[1][0][0]['url'], playlistName2= url[1][1], songsNum2=url[1][2], url3=url[2][0][0]['url'], playlistName3= url[2][1], songsNum3=url[2][2])

@app.route("/<usr>")
def user(usr):
    return f"<h1>Congratulations {usr} has been created</h1>"

@app.route("/vibe", methods=["POST", "GET"])
def vibe():
    if request.method == "POST":
        print("I am here")
        newVibe = {"name" : request.form["VibeName"], "acousticness" : request.form["acousticness"], "danceability" : request.form["danceability"],
        "energy" : request.form["energy"], "tempo" : request.form["tempo"], "valence" : request.form["valence"]}

        print(newVibe)
        session["vibe"] = newVibe
        spotifyObject = Spotify(auth=session["token"])
        spotifyUser = spotifyObject.current_user()
        spotifyID = spotifyUser["id"]
        #newUser = users(username=spotifyID)#test
        #db.session.add(newUser)#this
        #db.session.commit()#out
        found_user = users.query.filter_by(username = spotifyID).first() #how to make a new user!!!?
        if found_user:
            print("found the new user")
            if len(found_user.mood) > 0:
                print("will it work?")
                print(found_user.mood)
                print("i did it")
        else:
            newUser = users(username=spotifyID)
            db.session.add(newUser)
            db.session.commit()
            found_user = users.query.filter_by(username=spotifyID).first()
            print("what")
            mood1 = Mood(request.form["VibeName"], int(request.form["acousticness"]), int(request.form["danceability"]),
                        int(request.form["energy"]), int(request.form["tempo"]), int(request.form["valence"]), user_id=found_user.id)
            print("up")
            db.session.add(mood1)
            print("yall")
            db.session.commit()
            print("work?")
        return redirect(url_for("user", usr=session["vibe"]["name"]))

    else:
        print("What")
        return render_template("spotifyVibeMaker.html") #create vibe page

@app.route("/")
def login():
    return render_template("SpotifyCreate Page.html") # redirects you through to the name function
#https://accounts.spotify.com/authorize?client_id=0564e53d485643aaa292796e7d73cc43&response_type=code&redirect_uri=http%3A%2F%2Fspotifypro.pythonanywhere.com&scope=user-read-email%20playlist-read-private%20playlist-modify-private%20playlist-modify-public

db.create_all()

if __name__ == '__main__':
    app.run()

