import webapp2
from google.appengine.ext import ndb
import logging
import os

from top_albums_list_extractor import get_top_albums_billboard, get_top_albums_billboard_2, get_top_albums_itunes
from album_tracklist_extractor_and_selector import get_random_track
from artists_from_song import get_artists_fr_song
from lyric_extractor import get_lyrics
from one_line_lyric_extractor import get_one_lyric

from data_classes import OneLineLyric, Song, Artist

class OneLineHandler(webapp2.RequestHandler):
    def get(self):
        # Three dictionaries contain three different lists of the 'top' hiphop/rap albums
        album_dict1 = get_top_albums_billboard()
        album_dict2 = get_top_albums_billboard_2()
        album_dict3 = get_top_albums_itunes()

        for album_name in album_dict1:
            artist_name = album_dict1[album_name]
            # This retrieves a random track from the selected album
            random_track = get_random_track(artist_name,album_name)
            artist_list = 







app = webapp2.WSGIApplication([
    ('/crons/oneline',OneLineHandler)
], debug=True)
