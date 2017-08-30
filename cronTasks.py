from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from data_classes import OneLineLyric, Song, Artist
import logging


from top_albums_list_extractor import get_top_albums
from album_tracklist_extractor_and_selector import get_random_track
from artists_from_song import get_artists_fr_song
from lyric_extractor import get_lyrics
from one_line_lyric_extractor import get_one_lyric

print get_lyrics("Tyler, The Creator","Boredom")

class OneLineHandler(webapp2.RequetHandler):
    def get(self):
        self.response.write('sup')




app = webapp2.WSGIApplication([
    ('/task/cron/oneline',OneLineHandler)
], debug=True)

if __name__ == '__cronTasks__':
    run_wsgi_app(app)
