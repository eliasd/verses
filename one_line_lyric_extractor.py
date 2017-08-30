import re
import urllib2
# This is placed here in order to manually include the outside library 'bs4' from the lib directory
import sys
sys.path.insert(0, 'lib')
from bs4 import BeautifulSoup
import random

# Part of 'album_track_lyric_search_functions'
#parses through a song's lyrics and randomly returns one line from the track
def get_one_lyric(song_lyrics):
    try:
        line_list = song_lyrics.split("\n")
        # number_of_lines = song_lyrics.count("\n")+1
        # random_line = random.randint(0,number_of_lines+1)
        #
        # current_line = 0
        # line_break_index = song_lyrics.find("\n")
        # while(current_line<random_line):
        #     line_break_index = song_lyrics.find("\n",line_break_index+1)
        # while(line_list.index("")>=0):
        #     del line_list[line_list.index(" ")]
        line_list_length = len(line_list)
        random_line_index = random.randint(0,line_list_length)

        while(line_list[random_line_index]=='' or line_list[random_line_index].find("<i>")>=0):
            random_line_index = random.randint(0,line_list_length)

        return line_list[random_line_index]
    except Exception as e:
        return "Exception occurred \n" +str(e)


# lyric = get_lyrics("Tyler, The Creator","Where This Flower Blooms")
#
# print get_one_lyric(lyric)
