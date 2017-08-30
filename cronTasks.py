import webapp2
from google.appengine.ext import ndb
import logging
import os

from top_albums_list_extractor import get_top_albums_billboard
from album_tracklist_extractor_and_selector import get_random_track
from artists_from_song import get_artists_fr_song
from lyric_extractor import get_lyrics
from one_line_lyric_extractor import get_one_lyric

from data_classes import OneLineLyric, Song, Artist


class OneLineHandler(webapp2.RequestHandler):
    def get(self):
        lyric = get_lyrics("Tyler, The Creator","Where This Flower Blooms")

        logging.info(get_one_lyric(lyric))

app = webapp2.WSGIApplication([
    ('/crons/oneline',OneLineHandler)
], debug=True)
