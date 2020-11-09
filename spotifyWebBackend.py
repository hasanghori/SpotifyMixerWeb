import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from refreshToken import Refresh
from SpotifySecret import client_id, client_secret, redirect_uri
from pprint import pprint
import requests
import json


class songObject:
    def __init__(self, uri, acousticness, danceability, energy, tempo,
                 valence):
        self.uri = uri
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.tempo = tempo
        self.valence = valence

class PlaylistCreation:
    def createObjectsList(self, songIDList, spotifyObject):
        songObjectsList = []
        for i in range(0, len(songIDList)):
            songFeatures = spotifyObject.audio_features(songIDList[i])
            songObj = songObject(songIDList[i], acousticness=songFeatures[0]['acousticness'],
                                 danceability=songFeatures[0]['danceability'], energy=songFeatures[0]['energy'],
                                 tempo=songFeatures[0]['tempo'], valence=songFeatures[0]['valence'])
            songObjectsList.append(songObj)
        return songObjectsList


    def carVibes(self, songObj):
        carVibeness = int(songObj.tempo + (songObj.energy * 190) + (songObj.danceability * 190))
        return carVibeness


    def sadBoiHours(self, songObj): #relax playlist
        sadBoiHoursNess = int(-(songObj.tempo * 1.7) - (songObj.energy * 180) - (songObj.danceability * 190)
                              - (songObj.valence * 200))
        return sadBoiHoursNess


    def workout(self, songObj):
        workoutAbility = int((songObj.tempo * 1.5) + (songObj.energy * 190) + (songObj.danceability * 90))
        return workoutAbility


    def vibeDecider(self, song, vibe):
        if vibe == 1:
            return self.carVibes(song)
        elif vibe == 3:
            return self.sadBoiHours(song)
        else:
            return self.workout(song)


    def quickSort(self, songObjectsList, vibe):
        length = len(songObjectsList)
        if length <= 1:
            return songObjectsList
        else:
            pivot = songObjectsList.pop()

        songs_higher = []
        songs_lower = []

        for song in songObjectsList:
            if self.vibeDecider(song, vibe) > self.vibeDecider(pivot, vibe):
                songs_higher.append(song)
            else:
                songs_lower.append(song)

        return self.quickSort(songs_higher, vibe) + [pivot] + self.quickSort(songs_lower, vibe)

    def getPlaylistImage(self, token):
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']
        playlistDetails = [[0 for playlists in range(3)] for items in range(3)]
        for count in range(0, 3):
            try:
                response = spotifyObject.user_playlists(user=username, limit=1, offset=count)

                playlistID = response['items'][0]['id']
                playlistDetails[count][0] = spotifyObject.playlist_cover_image(playlist_id=playlistID) #img
                playlistDetails[count][1] = response['items'][0]['name'] #name
                playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
                playlistDetails[count][2] = playlist['total'] #numSongs
            except:
                break


        return playlistDetails

    def loadPlaylists(self, token):
        print("test1")
        spotifyObject = Spotify(auth=token)
        print("test2")
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']
        print("test3")
        playlistProperties = {}
        print("test4")
        response = spotifyObject.user_playlists(user=username, limit=1)
        print("test5")
        numOfPlaylists = response['total']
        print("test6")
        count = int(0)

        while (200 > count):
            response = spotifyObject.user_playlists(user=username, limit=1, offset=count)
            count = count + 1
            print(response['items'][0]['name'])
            playlistProperties[response['items'][0]['name']] = response['items'][0]['id']

        return playlistProperties

    def mainMethod(self, playlistName, vibe, playlist_name, token):
        #authorization
        spotifyObject = Spotify(auth=token)
        spotifyUser = spotifyObject.current_user()
        username = spotifyUser['id']


        #finding the playlist
        response = spotifyObject.user_playlists(user=username, limit=1)
        numOfPlaylists = response['total']
        count = int(0)
        while (numOfPlaylists > count):
            if (playlistName == response['items'][0]['name']):
                break
            response = spotifyObject.user_playlists(user=username, limit=1, offset=count)
            count = count + 1
        playlistID = response['items'][0]['id']


        #finding and sorting tracks based on the vibe
        playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID)
        numberOfSongs = int(playlist['total'])
        totalAdded = int(0)
        songURIS = []
        while (numberOfSongs > totalAdded):
            playlist = spotifyObject.user_playlist_tracks(user=username, playlist_id=playlistID,offset=totalAdded)
            for i in range(0, len(playlist['items'])):
                songURIS.append(playlist['items'][i]['track']['uri']) #id
            totalAdded = totalAdded + 100

        songObjectsList = []
        songObjectsList = self.createObjectsList(songIDList= songURIS, spotifyObject=spotifyObject)

        sortedSongsList = self.quickSort(songObjectsList, int(vibe))
        
        numSongs = int(25)
        songsToAdd = []
        print(len(sortedSongsList))
        for songs in range(0, int(numSongs)):
            try:
                songsToAdd.append(sortedSongsList[songs].uri)
            except:
                break

        spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True)
        prePlaylist = spotifyObject.user_playlists(user=username)
        playlist = prePlaylist['items'][0]['id']

        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=songsToAdd)
