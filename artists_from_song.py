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
    artist_original = artist
    artist_copy1 = ""
    artist_copy2 = ""
    if(artist.find('and')>=0):
        artist_copy1 = artist.replace('and','&')
        artist_copy2 = artist.replace('and','And')
    elif(artist.find("And")>=0):
        artist_copy1 = artist.replace('And','&')
        artist_copy2 = artist.replace('And','and')
    else:
        artist_copy1 = artist.replace('&','and')
        artist_copy2 = artist.replace('&','And')

    artist_list.append(artist)

    #loops through and produces an artist string that is usuable in the url search
    artist = artist.lower()
    artist = artist.capitalize()
    artist_split_list = artist.split(" ")
    artist = ""
    for n in range(0,len(artist_split_list)):
        #all instances of a period are deleted and '&' and 'é' are replaced
        artist_split_list[n] = artist_split_list[n].replace(".","").replace("&","and").replace("é","e")
        #all other non-alphanumeric characters are replaced by a '-'
        #these include: "-","$",","
        artist_split_list[n] = re.sub('[^A-Za-z0-9]+',"-",artist_split_list[n])
        len_of_word = len(artist_split_list[n])
        if n==0 and artist_split_list[n][0:1] == "-":
            artist += artist_split_list[n][1:]
        elif len_of_word==1 and artist_split_list[n] == "-":
            continue
        elif artist_split_list[n][len_of_word-1:len_of_word] == "-" and n!=len(artist_split_list)-1:
            artist += artist_split_list[n]
        elif n==len(artist_split_list)-1 and artist_split_list[n][len_of_word-1:len_of_word] == "-":
            artist += artist_split_list[n][0:len_of_word-1]
        elif n==len(artist_split_list)-1 and artist_split_list[n][len_of_word-1:len_of_word] != "-":
            artist += artist_split_list[n]
        else:
            artist += artist_split_list[n]+"-"

    #loops through and produces a song_title string that is usuable in the url search
    song_title = song_title.lower()
    song_split_list = song_title.split(" ")
    song_title = ""
    for n in range(0,len(song_split_list)):
        song_split_list[n] = song_split_list[n].replace("'","").replace("&","and").replace(".","").replace("(","").replace(")","")
        song_split_list[n] = re.sub('[^A-Za-z0-9]+',"-",song_split_list[n])
        len_of_word = len(song_split_list[n])
        if n==0 and song_split_list[n][0:1] == "-":
            song_title += song_split_list[n][1:]
        elif len_of_word==1 and song_split_list[n] == "-":
            continue
        elif song_split_list[n][len_of_word-1:len_of_word] == "-" and n!=len(song_split_list)-1:
            song_title += song_split_list[n]
        elif n==len(song_split_list)-1 and song_split_list[n][len_of_word-1:len_of_word] == "-":
            song_title += song_split_list[n][0:len_of_word-1]
        elif n==len(song_split_list)-1 and song_split_list[n][len_of_word-1:len_of_word] != "-":
            song_title += song_split_list[n]
        else:
            song_title += song_split_list[n]+"-"

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
            artist_name = artist_name.replace("&amp;","&").replace("\xe2\x80\x8b","")

            # This checks if the artist is already in the list and that it doesn't have any copies in the list with small variations
            # E.G. 'Nav And Metro Boomin' vs 'Nav & Metro Boomin'
            if artist_name not in artist_list and artist_name.lower()!=artist_original.lower() and artist_name.lower()!=artist_copy1.lower() and artist_name.lower()!=artist_copy2.lower():
                artist_list.append(artist_name)
                print artist_list
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

        featured_artists = featured_artists.replace("&amp;","&")
        return featured_artists
    except Exception as e:
        return "Exception occurred \n123"

print get_artists_fr_song("Blackbear","I miss the old u")
