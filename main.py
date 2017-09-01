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
import json
from google.appengine.ext import ndb
from data_classes import OneLineLyric, Song, Artist
import random

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


##NOTICE: BUILD CRON FILE
def randomIndex(a,b):
    return random.randint(a,b-1)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # NOTICE: These were temporarily stored in Datastore in order to test ajax
        #   Ultimately, this section would randomly retrieve Datastore elements that were already stored in the Database
        #   due to the Cron Tab and Execution (as opposed to manually storing them here)
        #------------------------------------------------------------------------------------------------------#
        # artist_temp = Artist(name = "BROCKHAMPTON")
        # artist_temp_key = artist_temp.put()
        # song_temp = Song(title = "GOLD", artist_key = artist_temp_key)
        # song_temp_key = song_temp.put()
        # one_line_lyric_temp = OneLineLyric(lyric_text="Grab life by the horns when I whip the Lambo",vote_count=0,song_key=song_temp_key,artist_key=artist_temp_key,feat_artist='')
        # lyric_key = one_line_lyric_temp.put()
        # #
        # artist_temp = Artist(name = "Kendrick Lamar")
        # artist_temp_key = artist_temp.put()
        # song_temp = Song(title = "FEEL.", artist_key = artist_temp_key)
        # song_temp_key = song_temp.put()
        # one_line_lyric_temp = OneLineLyric(lyric_text="Ain't nobody prayin' for me",vote_count=0,song_key=song_temp_key,artist_key=artist_temp_key,feat_artist='')
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
            'feat_artist_left': left_lyric_el.feat_artist,

            'lyric_right': right_lyric_el.lyric_text,
            'song_name_right':right_song_el.title,
            'artist_name_right':right_artist_el.name,
            'feat_artist_right':right_lyric_el.feat_artist

        }

        self.response.write(template.render(main_template_variables))

class VoteHandler(webapp2.RequestHandler):
    def post(self):
        #HERE The handler recieves the json data and extracts the specific datastore objects that matche the json data
        # The data that must match includes: Artist name, song-name, and lyric
        # NOTICE: Encoding issues may arise here in 'json.loads' due to specific non-ASCII characters; you may
        #  have to specify an encoding name here (check 'json.loads' documentation)
        # Possible solution:    data_unicode = request.body.decode('utf-8')
        #                       data = json.loads(data_unicode)
        data = json.loads(self.request.body)
        artist_selected = Artist.query(Artist.name==data["artist-name-selected"]).get()
        song_selected = Song.query(Song.title==data["song-name-selected"] and Song.artist_key==artist_selected.key).get()
        lyric_selected = OneLineLyric.query(OneLineLyric.lyric_text==data["lyric-selected"] and OneLineLyric.song_key==song_selected.key and OneLineLyric.artist_key==artist_selected.key).get()

        artist_unselected = Artist.query(Artist.name==data["artist-name-unselected"]).get()
        song_unselected = Song.query(Song.title==data["song-name-unselected"] and Song.artist_key==artist_unselected.key).get()
        lyric_unselected = OneLineLyric.query(OneLineLyric.lyric_text==data["lyric-unselected"] and OneLineLyric.song_key==song_unselected.key and OneLineLyric.artist_key==artist_unselected.key).get()

        #NOTICE | IMPORTANT: HERE, THE vote count of the selected lyric would increase in the database but in order to preserve the data
        # for testing, it is commented out until the vote count will be used later for the Trending Page
        #lyric_selected.vote_count += 1
        #lyric_selected.put()

        #NOTICE: THIS SECTION randomly selects TWO new One Line Lyric that are different from either of the lyrics
        # already on the page in order to replace BOTH the Left and Right side lyrics
        lyric_list = OneLineLyric.query().fetch()
        list_len = len(lyric_list)
        random_index_sel = randomIndex(0,list_len)
        random_index_unsel = randomIndex(0,list_len)
        while(random_index_sel==random_index_unsel or lyric_list[random_index_sel].key==lyric_selected.key or lyric_list[random_index_sel].key==lyric_unselected.key or
            lyric_list[random_index_unsel].key==lyric_unselected.key or lyric_list[random_index_unsel].key==lyric_unselected.key):
            random_index_sel = randomIndex(0,list_len)
            random_index_unsel = randomIndex(0,list_len)

        lyric_sel = lyric_list[random_index_sel]
        song_sel = Song.query(Song.key == lyric_sel.song_key).get()
        artist_sel = Artist.query(Artist.key == lyric_sel.artist_key).get()
        #If feat_artist is not an empty string, a new string is combined so that it includes 'ft.'
        featured_artist_sel = ""
        if lyric_sel.feat_artist:
            featured_artist_sel = "(ft. %s)" % lyric_sel.feat_artist
        else:
            featured_artist_sel = ""


        lyric_unsel = lyric_list[random_index_unsel]
        song_unsel = Song.query(Song.key == lyric_unsel.song_key).get()
        artist_unsel = Artist.query(Artist.key == lyric_unsel.artist_key).get()
        #If feat_artist is not an empty string, a new string is combined so that it includes 'ft.'
        featured_artist_unsel = ""
        if lyric_unsel.feat_artist:
            featured_artist_unsel = "(ft. %s)" % lyric_unsel.feat_artist
        else:
            featured_artist_unsel = ""



        # NOTICE: This data dictionary sends this info to the JS side
        self.response.out.write(json.dumps((
            {
            'lyric-selected': lyric_sel.lyric_text,
            'song-name-selected':song_sel.title,
            'artist-name-selected':artist_sel.name,
            'feat-artist-selected':featured_artist_sel,
            'lyric-unselected':lyric_unsel.lyric_text,
            'song-name-unselected':song_unsel.title,
            'artist-name-unselected':artist_unsel.name,
            'feat-artist-unselected':featured_artist_unsel
            })))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vote/',VoteHandler)
], debug=True)
