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

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


##BUILD CRON FILE

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/main.html')

        main_template_variables = {
            'lyric_left': 'I rock, I roll, I bloom, I glow',
            'song_name_left': 'Where This Flower Blooms',
            'artist_name_left': 'Tyler, The Creator',
            'lyric_right':"Ain't nobody prayin' for me",
            'song_name_right':'FEEL.',
            'artist_name_right':'Kendrick Lamar'
        }

        self.response.write(template.render(main_template_variables))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
