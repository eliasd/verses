# -*- coding: utf-8 -*-
import re
import urllib2
# This is placed here in order to manually include the outside library 'bs4' from the lib directory
import sys
sys.path.insert(0, 'lib')
from bs4 import BeautifulSoup

# # Part of 'album_track_lyric_search_functions'
def get_lyrics(artist,song_title):
    artist = artist.lower()
    artist = artist.capitalize()
    artist_split_list = artist.split(" ")
    artist = ""
    #loops through and produces an artist string that is usuable in the url search
    for n in range(0,len(artist_split_list)):
        #all instances of a period are deleted and '&' and 'é' are replaced
        artist_split_list[n] = artist_split_list[n].replace(".","").replace("&","and").replace("é","e")
        #all other non-alphanumeric characters are replaced by a '-'
        #these include: "-","$",","
        artist_split_list[n] = re.sub('[^A-Za-z0-9]+',"-",artist_split_list[n])
        len_of_word = len(artist_split_list[n])
        if n==0 and artist_split_list[n][0:1] == "-":
            artist += artist_split_list[n][1:]
        elif len_of_word==1 and artistm_split_list[n] == "-":
            continue
        elif artist_split_list[n][len_of_word-1:len_of_word] == "-" and n!=len(artist_split_list)-1:
            artist += artist_split_list[n]
        elif n==len(artist_split_list)-1 and artist_split_list[n][len_of_word-1:len_of_word] == "-":
            artist += artist_split_list[n][0:len_of_word-1]
        elif n==len(artist_split_list)-1 and artist_split_list[n][len_of_word-1:len_of_word] != "-":
            artist += artist_split_list[n]
        else:
            artist += artist_split_list[n]+"-"

    song_title = song_title.lower()
    song_split_list = song_title.split(" ")
    song_title = ""
    #loops through and produces a song_title string that is usuable in the url search
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
        lyric_page = str(soup)

        up_partition = '<div class="lyrics">'
        down_partition = '<div initial-content-for="recirculated_content">'
        lyric_page = lyric_page.split(up_partition)[1]
        lyric_page = lyric_page.split(down_partition)[0]
        up_partition = '<!--sse-->'
        down_partition = '<!--/sse-->'
        lyric_page = lyric_page.split(up_partition)[1]
        lyric_page = lyric_page.split(down_partition)[0]
        lyric_page = lyric_page.replace('</i>','').replace('<i>','').replace("</a>","").replace("<p>","").replace("</p>","").replace("<br/>","")
        no_more_a_tags = False
        while(no_more_a_tags==False):
            if lyric_page.find("<a")>=0:
                front_index = lyric_page.find("<a")
                end_index = lyric_page.find(">",front_index)
                lyric_page = lyric_page[:front_index] + "" + lyric_page[end_index+1:]
            else:
                no_more_a_tags = True
        # Returns a list of the lyrics with each line being a seperate element
        lyric_list = lyric_page.split("\n")
        return lyric_list
    except Exception as e:
        return "Exception occurred \n" +str(e)

def get_lyrics2(artist,song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"

    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('<br/>','').replace('</div>','').strip()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" +str(e)

# Test a little more
print get_lyrics("Kendrick Lamar","lOYALTY.")
