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
        # one_line_lyric_temp = OneLineLyric(lyric_text="I rock, I roll, I bloom, I glow",upvotes=0,song_key=song_temp_key,artist_key=artist_temp_key)
        # lyric_key = one_line_lyric_temp.put()
        #
        # artist_temp = Artist(name = "Kendrick Lamar")
        # artist_temp_key = artist_temp.put()
        # song_temp = Song(title = "FEEL.", artist_key = artist_temp_key)
        # song_temp_key = song_temp.put()
        # one_line_lyric_temp = OneLineLyric(lyric_text="Ain't nobody prayin' for me",upvotes=0,song_key=song_temp_key,artist_key=artist_temp_key)
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

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
