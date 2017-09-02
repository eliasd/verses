import re
import urllib2
# This is placed here in order to manually include the outside library 'bs4' from the lib directory
import sys
sys.path.insert(0, 'lib')
from bs4 import BeautifulSoup
import random
from HTMLParser import HTMLParser

# Part of 'album_track_lyric_search_functions'
#finds the tracks within an album and then randomly selects one track and returns the title of that track
def get_random_track(artist,album):
    # This removes any 'deluxe' or 'remastered' tags from the album name
    album = album.replace(' (Deluxe)','').replace(' (Deluxe Version)','').replace(' (Remastered)','').replace(' - EP','')
    album = album.lower()
    album = album.capitalize()
    #the album name is split into a list in order to remove unnecessary characters for the url
    album_split_list = album.split(" ")
    album = ""
    for n in range(0,len(album_split_list)):
        album_split_list[n] = re.sub('[^A-Za-z0-9]+',"-",album_split_list[n])
        len_of_word = len(album_split_list[n])
        if n==0 and album_split_list[n][0:1] == "-":
            album += album_split_list[n][1:]
        elif len_of_word==1 and album_split_list[n] == "-":
            continue
        elif album_split_list[n][len_of_word-1:len_of_word] == "-" and n!=len(album_split_list)-1:
            album += album_split_list[n]
        elif n==len(album_split_list)-1 and album_split_list[n][len_of_word-1:len_of_word] == "-":
            album += album_split_list[n][0:len_of_word-1]
        elif n==len(album_split_list)-1 and album_split_list[n][len_of_word-1:len_of_word] != "-":
            album += album_split_list[n]
        else:
            album += album_split_list[n]+"-"

    artist = artist.lower()
    artist = artist.capitalize()
    # remove all except alphanumeric characters from artist
    artist = re.sub('[^A-Za-z0-9]+', "-", artist)
    url = "http://genius.com/albums/"+artist+"/"+album

    try:
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36' }
        req = urllib2.Request(url,None,headers)
        content = urllib2.urlopen(req).read()
        soup = BeautifulSoup(content, 'html.parser')
        album_page = str(soup)

        # lyrics lies between up_partition and down_partition
        up_partition = '<div class="column_layout u-top_margin">'
        down_partition = '<div class="footer">'
        album_page = album_page.split(up_partition)[1]
        album_page = album_page.split(down_partition)[0]

        #current_index is first set to the index at which the name of the album is found
        current_index = album_page.find('<h3 class="chart_row-content-title">')
        len_front_tag = len('<h3 class="chart_row-content-title">')
        track_list = []
        no_more_tracks = False
        while(no_more_tracks==False):
            #current_index is set to the first front-tag index as it is necessary in
            # # order to find the end-index of the front tag (right before the artist name)
            current_index = album_page.find('<h3 class="chart_row-content-title">',current_index)
            if current_index < 0:
                break
            #this is the the index immediately after the track name (end tag)
            album_end_index = album_page.find('<span',current_index)

            #extracts the song title and removes annoying whitespace
            song_title = album_page[current_index+len_front_tag:album_end_index].strip()
            #if the song has any features it removes the string of the 'feat'
            song_title = song_title.replace("(Album Version)","")
            if song_title.find(' (Ft.')>=0:
                front_index = song_title.find('(Ft.')
                song_title = song_title[0:front_index]

            song_title = song_title.strip()
            # #Decoding html entities in python string by simply replacing it
            #NOTICE: CONSIDER moving the decoding into main.py
            # song_title = song_title.replace('&amp;','&')
            song_title = song_title.replace('\xc2','').replace('\xa0','').replace('\xe2','').replace("\x80",'').replace('\x8b','')
            track_list.append(song_title)
            # current_index is updated to proceed down the html page
            current_index=current_index+1
            # checks to make sure that its the last track on the album
            check_for_track_index = album_page.find('<span class="chart_row-number_container-number chart_row-number_container-number',current_index)
            end_check_index = album_page.find('</span>',check_for_track_index)
            if album_page.find('<span></span>',check_for_track_index,end_check_index+10)>=0:
                break


        #at this point, track_list has been completely filled with the all tracks related to album at hand
        track_length = len(track_list)
        random_index = random.randint(0,track_length-1)
        return track_list[random_index]
    except Exception as e:
        return "Exception occurred \n"

def get_random_track2(artist,album):
    # This removes any 'deluxe' or 'remastered' tags from the album name
    album = album.replace(' (Deluxe)','').replace(' (Deluxe Version)','').replace(' (Remastered)','')
    artist = artist.lower()
    first_letter_artist_name = artist[0:1]
    if(first_letter_artist_name.isdigit()):
        first_letter_artist_name='19'
    # remove all except alphanumeric characters from artist
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/"+first_letter_artist_name+"/"+artist+".html"

    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        album_list_page = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- start of song list -->'
        down_partition = '<script type="text/javascript">'
        album_list_page = album_list_page.split(up_partition)[1]
        album_list_page = album_list_page.split(down_partition)[0]
        album_list_page = album_list_page.replace('<br>','').replace('</br>','').replace('</div>','').strip()

        #current_index is first set to the index at which the name of the album is found
        current_index = album_list_page.find(album)
        track_list = []
        no_more_tracks = False
        while(no_more_tracks==False):
            #current_index is set to the first front-tag index as it is necessary in
            # order to find the end-index of the front tag (right before the artist name)
            current_index = album_list_page.find('<a href=',current_index)
            end_artist_front_tag_index = album_list_page.find('>',current_index)
            #this is the the index immediately after the artist name (end tag)
            beginning_artist_end_tag_index = album_list_page.find('<',end_artist_front_tag_index)

            song_title = album_list_page[end_artist_front_tag_index+1:beginning_artist_end_tag_index]

            track_list.append(song_title)
            # current_index is updated to proceed down the html page
            current_index=current_index+1

            #this checks if there are any more tracks left in the album by seeing if there is a div or anchor "id" tag
            # immediately following the last tag of the line (a div tag or anchor "id" tag has to be within 15 characters of
            # the last tag)
            last_line_tag_index = album_list_page.find('>',beginning_artist_end_tag_index+5)
            if(album_list_page.find('<div class',last_line_tag_index,last_line_tag_index+15)>=0 or album_list_page.find('<a id',last_line_tag_index,last_line_tag_index+15)>=0):
                no_more_tracks==True
                break

        #at this point, track_list has been completely filled with the all tracks related to album at hand
        track_length = len(track_list)
        random_index = random.randint(0,track_length-1)
        return track_list[random_index]
    except Exception as e:
        return "Exception occurred \n"

print get_random_track('Kendrick Lamar','DAMN.')
