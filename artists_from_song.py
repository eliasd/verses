# -*- coding: utf-8 -*-
import re
import urllib2
# This is placed here in order to manually include the outside library 'bs4' from the lib directory
import sys
sys.path.insert(0, 'lib')
from bs4 import BeautifulSoup

# Part of 'album_track_lyric_search_functions'
#retreives all artists featured on the song
#retreives from Genius.com
def get_artists_fr_song(artist,song_title):
    artist_list = []
    if(artist.find('&')>=0):
        artist_copy = artist.replace('&','&amp;')
        artist_list.append(artist_copy)
    else:
        artist_list.append(artist)

    artist = artist.lower()
    artist = artist.capitalize()
    song_title = song_title.lower()
    #FUTURE_IDEA: you can take each word from the song_title and artist name split it into a list (.split()), remove all
    # non-alphanumeric characters with the easy solution (re.sub('[^A-Za-z0-9]+', "-", artist/song_title))
    # and then simply form a new string in which each word is seperated by a "-"

    artist = artist.replace("&","and").replace("é","e")
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "-", artist)

    #Here I am deleting specific non-alphanumeric characters (can't just generally replace all of them with "-"
    # as certain characters like the apostrophe occur right in the middle of a word and a replacement there
    # would mess up the url
    song_title = song_title.replace("'","").replace("&","and").replace(".","").replace("(","").replace(")","")
    song_title = song_title.replace(" ","-")
    url = "https://genius.com/"+artist+"-"+song_title+"-lyrics"

    try:
        #note that User-Agent header is required since Genius returns 403 - Forbidden without it
        headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' }
        req = urllib2.Request(url, None, headers)
        content = urllib2.urlopen(req).read()
        soup = BeautifulSoup(content, 'html.parser')
        song_info = str(soup)

        list_is_closed = False
        start_index = song_info.find('artists&quot;:[')
        front_index = song_info.find('&quot;',start_index+15)
        end_index = song_info.find('&quot;',front_index+1)
        while(list_is_closed==False):
            #THE LOOP NEEDS TO BE FIXED
            artist_name = song_info[front_index+6:end_index]
            if artist_name not in artist_list:
                artist_list.append(artist_name)
            if song_info[end_index+6:end_index+7]==']':
                list_is_closed = True
            else:
                front_index = song_info.find('&quot;',end_index+1)
                end_index = song_info.find('&quot;',front_index+1)

        featured_artists = ""
        if len(artist_list) == 1:
            featured_artists = ""
        elif len(artist_list) == 2:
            featured_artists = artist_list[1]
        else:
            last_index = len(artist_list)-1
            for n in range(1,len(artist_list)):
                if n!=last_index:
                    featured_artists+=artist_list[n]+", "
                else:
                    featured_artists+=artist_list[n]

        return featured_artists
    except Exception as e:
        return "Exception occurred \n" +str(e)

# print get_artists_fr_song("A$AP Mob","RAF")
