import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import credentials

username = credentials.username

class MusicBot:
    def __init__(self, sm):
        self.token = util.prompt_for_user_token(username) # Check Spotipy doc to setup your own app.
        self.sp = spotipy.Spotify(auth=self.token) 
        self.sm = sm
        self.current_track = ''
    
    def search(self, request):
        res = self.sp.search(q=request, type='track')

        if len(res) > 0:
            track_uri = res['tracks']['items'][0]['uri']
            track_name = res['tracks']['items'][0]['name']
            artist_name = res['tracks']['items'][0]['artists'][0]['name']
            print(track_uri, track_name, artist_name)
            self.play_song(track_uri, track_name, artist_name)
        else:
            self.sm.send_text_message('Désolé, aucune musique trouvée pour ' + request)
    
    def play_song(self, uri, name, artist):
        self.current_track = name
        self.sp.start_playback(uris=[uri])
        self.sm.send_text_message('Titre trouvé : ' + name + ' par ' + artist + ' ...le titre commence')
    
    def pause(self):
        self.sp.pause_playback()
        self.sm.send_text_message('Le titre ' + self.current_track + ' a ete mis en pause !')
        
    def resume(self):
        if self.current_track != '':
            try:
                self.sp.start_playback()
                self.sm.send_text_message('Le titre ' + self.current_track + ' reprend !')
            except spotipy.exceptions.SpotifyException:
                print('le player pas lancé')
        else:
            self.sm.send_text_message('Aucun titre joue pour le moment')


    def command(self, content):
        if content.startswith('pause'):
            self.pause()
        if content.startswith('resume'):
            self.resume()
        if content.startswith('resume') == False and content.startswith('pause') == False:
            self.search(content)

