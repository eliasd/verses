import re
import urllib2
# This is placed here in order to manually include the outside library 'bs4' from the lib directory
#
import sys
sys.path.insert(0, 'lib')
from bs4 import BeautifulSoup

# Part of 'album_track_lyric_search_functions'
#returns a dictionary of the top 50 hip-hop/r&b albums on the billboard charts with the albums defining the artist names
def get_top_albums_billboard():
    url = "http://www.billboard.com/charts/r-b-hip-hop-albums"
    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        album_page = str(soup)

        albums_dict = {}
        #current_index refers to the starting index at which album_page is searched
        current_index = 0
        #length of the album header right before the album name
        beginning_album_front_tag_length = len('<h2 class="chart-row__song">')

        no_more_albums = False
        while(no_more_albums==False):
            current_index = album_page.find('<h2 class="chart-row__song">',current_index)
            if(current_index<0):
                no_more_albums = True
                break;
            #the index that is immediately after the album name (end tag)
            front_album_end_tag_index = album_page.find('</h2>',current_index)
            #the album name is sliced out from between the front <h2....> and the back </h2>
            album_name = album_page[(current_index+beginning_album_front_tag_length):front_album_end_tag_index]

            #first front-tag index is necessary in order to find the end-index of the front tag
            beginning_artist_front_tag_index = album_page.find('<a class="chart-row__artist"',current_index)
            end_artist_front_tag_index = album_page.find('>',beginning_artist_front_tag_index)
            #this is the the index immediately after the artist name (end tag)
            beginning_artist_end_tag_index = album_page.find('<',end_artist_front_tag_index)

            artist_name = album_page[end_artist_front_tag_index+2:beginning_artist_end_tag_index-1]

            albums_dict[album_name] = artist_name
            #current_index is increased by one so the program can continue to search along the page, downwards
            current_index = current_index+1
        return albums_dict
    except Exception as e:
        return "Exception occurred \n" +str(e)

def get_top_albums_billboard_2():
    url = "http://www.billboard.com/charts/rap-albums"
    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        album_page = str(soup)

        albums_dict = {}
        #current_index refers to the starting index at which album_page is searched
        current_index = 0
        #length of the album header right before the album name
        beginning_album_front_tag_length = len('<h2 class="chart-row__song">')

        no_more_albums = False
        while(no_more_albums==False):
            current_index = album_page.find('<h2 class="chart-row__song">',current_index)
            if(current_index<0):
                no_more_albums = True
                break;
            #the index that is immediately after the album name (end tag)
            front_album_end_tag_index = album_page.find('</h2>',current_index)
            #the album name is sliced out from between the front <h2....> and the back </h2>
            album_name = album_page[(current_index+beginning_album_front_tag_length):front_album_end_tag_index]

            #first front-tag index is necessary in order to find the end-index of the front tag
            beginning_artist_front_tag_index = album_page.find('<a class="chart-row__artist"',current_index)
            end_artist_front_tag_index = album_page.find('>',beginning_artist_front_tag_index)
            #this is the the index immediately after the artist name (end tag)
            beginning_artist_end_tag_index = album_page.find('<',end_artist_front_tag_index)

            artist_name = album_page[end_artist_front_tag_index+2:beginning_artist_end_tag_index-1]

            albums_dict[album_name] = artist_name
            #current_index is increased by one so the program can continue to search along the page, downwards
            current_index = current_index+1
        return albums_dict
    except Exception as e:
        return "Exception occurred \n" +str(e)

def get_top_albums_itunes():
    url = "http://www.itunescharts.net/us/charts/albums/hip-hop/"
    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        album_page = str(soup)

        albums_dict = {}
        #current_index refers to the starting index at which album_page is searched
        current_index = 0
        #length of the tag right before the artist name
        beginning_artist_front_tag_length = len('<span class="entry">')
        artist_album_seperator_length = len(' - ')

        no_more_albums = False
        while(no_more_albums==False):
            current_index = album_page.find('<span class="entry">',current_index)
            if(current_index<0):
                no_more_albums = True
                break;
            #the index that is immediately after the artist name ()
            front_artist_end_tag_index = album_page.find(' - ',current_index)
            #the artist name is sliced out from between the front tag and the seperator ' - '
            artist_name = album_page[(current_index+beginning_artist_front_tag_length):front_artist_end_tag_index]

            #the index at which the album name starts
            end_album_front_tag_index = album_page.find(' - ',current_index)+artist_album_seperator_length
            # #this is the the index immediately after the album name (end tag)
            beginning_album_end_tag_index = album_page.find('<',end_album_front_tag_index)
            #
            album_name = album_page[end_album_front_tag_index:beginning_album_end_tag_index]
            #
            albums_dict[album_name] = artist_name
            #current_index is increased by one so the program can continue to search along the page, downwards
            current_index = current_index+1
        return albums_dict
    except Exception as e:
        return "Exception occurred \n" +str(e)

# print get_top_albums_itunes()
