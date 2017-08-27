#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import os
import webapp2
import logging
# Try (later) to figure out what exactly the module methods do
import json
import re
from google.appengine.ext import ndb
from data_classes import OneLineLyric, Song, Artist

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


##BUILD CRON FILE

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # NOTICE: These were temporarily stored in Datastore in order to test ajax
        #   Ultimately, this section would randomly retrieve Datastore elements that were already stored in the Database
        #   due to the Cron Tab and Execution (as opposed to manually storing them here)
        #------------------------------------------------------------------------------------------------------#
        # artist_temp = Artist(name = "Tyler, The Creator")
        # artist_temp_key = artist_temp.put()
        # song_temp = Song(title = "Where This Flower Blooms", artist_key = artist_temp_key)
        # song_temp_key = song_temp.put()
        # one_line_lyric_temp = OneLineLyric(lyric_text="I rock, I roll, I bloom, I glow",vote_count=0,song_key=song_temp_key,artist_key=artist_temp_key)
        # lyric_key = one_line_lyric_temp.put()
        #
        # artist_temp = Artist(name = "BROCKHAMPTON")
        # artist_temp_key = artist_temp.put()
        # song_temp = Song(title = "SWEET", artist_key = artist_temp_key)
        # song_temp_key = song_temp.put()
        # one_line_lyric_temp = OneLineLyric(lyric_text="Twistin' me up like licorice",vote_count=0,song_key=song_temp_key,artist_key=artist_temp_key)
        # lyric_key = one_line_lyric_temp.put()

        template = jinja_env.get_template('templates/main.html')

        #NOTICE: Here specific lyric elements are individually selected as opposed to the eventual random selection charateristic
        lyric_list = OneLineLyric.query().fetch()

        left_lyric_el = lyric_list[0]
        left_song_el = Song.query(Song.key == left_lyric_el.song_key).get()
        left_artist_el = Artist.query(Artist.key == left_lyric_el.artist_key).get()

        right_lyric_el = lyric_list[1]
        right_song_el = Song.query(Song.key == right_lyric_el.song_key).get()
        right_artist_el = Artist.query(Artist.key == right_lyric_el.artist_key).get()

        main_template_variables = {
            'lyric_left': left_lyric_el.lyric_text,
            'song_name_left': left_song_el.title,
            'artist_name_left': left_artist_el.name,

            'lyric_right': right_lyric_el.lyric_text,
            'song_name_right':right_song_el.title,
            'artist_name_right':right_artist_el.name
        }

        self.response.write(template.render(main_template_variables))

class VoteHandler(webapp2.RequestHandler):
    def post(self):
        #HERE The handler retreives the json data and extracts the specific datastore object that matches the json data
        # The data that must match includes: Artist name, song-name, and lyric
        data = json.loads(self.request.body)
        artist = Artist.query(Artist.name==data["artist-name"]).get()
        song = Song.query(Song.title==data["song-name"] and Song.artist_key==artist.key).get()
        lyric = OneLineLyric.query(OneLineLyric.lyric_text==data["lyric"] and OneLineLyric.song_key==song.key and OneLineLyric.artist_key==artist.key).get()

        #NOTICE: HERE, THE vote count of the selected lyric would increase in the database but in order to preserve the data
        # for testing, it is commented out until the vote count will be used later for the Trending Page
        #lyric.vote_count += 1
        #lyric.put()

        #NOTICE: THIS SECTION SHOULD randomly select a new One Line Lyric that is different from either of the lyrics
        # already on the page
        lyric_list = OneLineLyric.query().fetch()
        new_lyric = lyric_list[2]
        new_song = Song.query(Song.key == new_lyric.song_key).get()
        new_artist = Artist.query(Artist.key == new_lyric.artist_key).get()
        self.response.out.write(json.dumps((
            {
            'lyric': new_lyric.lyric_text,
            'song-name':new_song.title,
            'artist-name':new_artist.name
            })))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vote/',VoteHandler)
], debug=True)
