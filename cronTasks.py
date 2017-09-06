import webapp2
from google.appengine.ext import ndb
import logging
import os

from top_albums_list_extractor import get_top_albums_billboard, get_top_albums_billboard_2, get_top_albums_itunes
from album_tracklist_extractor_and_selector import get_random_track
from artists_from_song import get_artists_fr_song
from lyric_extractor import get_lyrics
from one_line_lyric_extractor import get_one_lyric

from data_classes import OneLineLyric, Song, Artist
from time import sleep

class OneLineHandler(webapp2.RequestHandler):
    def get(self):
        # Three dictionaries contain three different lists of the 'top' hiphop/rap albums
        album_dict1 = get_top_albums_billboard()
        album_dict2 = get_top_albums_billboard_2()
        album_dict3 = get_top_albums_itunes()

        for album_name in album_dict3:
            sleep(2)
            logging.info("ALBUM NAME:")
            logging.info(album_name)
            artist_name = album_dict3[album_name]

            # This retrieves a random track from the selected album
            random_track = get_random_track(artist_name,album_name)
            if random_track == "Exception occurred \n":
                logging.info("EXCEPTION 1")
                logging.info(album_name)
                logging.info(artist_name)
                continue
            logging.info("RANDOM TRACK:")
            logging.info(random_track)
            #retrieves a str of any featured artists on the song
            featured_artists_str = get_artists_fr_song(artist_name,random_track)
            if featured_artists_str == "Exception occurred \n123":
                logging.info("EXCEPTION 2")
                logging.info(album_name)
                logging.info(artist_name)
                logging.info(random_track)
                continue

            # This retreives the entire lyrics of a song
            lyrics = get_lyrics(artist_name,random_track)
            # This randomly selects one line lyric from the song
            one_line_lyric = get_one_lyric(lyrics)
            logging.info("ONE LINE LYRIC:")
            logging.info(one_line_lyric)
            if one_line_lyric == "Exception occured \n123":
                logging.info("EXCEPTION 3")
                logging.info(album_name)
                logging.info(artist_name)
                continue

            #Now have to make sure that this lyric/song/artist combination isn't a duplicate
            artist_el = Artist.query(Artist.name == artist_name).get()
            #If this artist is not in the database at all:
            if artist_el == None:
                new_artist = Artist(name = artist_name)
                new_artist_key = new_artist.put()
                new_song = Song(title=random_track,artist_key=new_artist_key,feat_artist=featured_artists_str)
                new_song_key = new_song.put()
                new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=new_song_key,artist_key=new_artist_key)
                new_one_line_lyric.put()
                continue
            else:
                artist_q_key = artist_el.key
                song_el = Song.query(Song.title==random_track and Song.artist_key == artist_q_key and Song.feat_artist == featured_artists_str).get()
                #If this artist is in the database but the song is not:
                if song_el == None:
                    new_song = Song(title=random_track,artist_key=artist_q_key,feat_artist=featured_artists_str)
                    new_song_key = new_song.put()
                    new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=new_song_key,artist_key=artist_q_key)
                    new_one_line_lyric.put()
                    continue
                else:
                    song_q_key = song_el.key
                    one_line_lyric_el = OneLineLyric.query(OneLineLyric.lyric_text==one_line_lyric and OneLineLyric.artist_key == artist_q_key and OneLineLyric.song_key == song_q_key).get()
                    # if this artist and song are in the database but the one-line-lyric is not:
                    if one_line_lyric_el == None:
                        new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=song_q_key,artist_key=artist_q_key)
                        new_one_line_lyric.put()
                        continue
                    else:
                        #if this artist and song and this one_line_lyric_el are in the database:
                        # Then try to find a new one-line-lyric from that song that isn't in the database or
                        # After 30 tries, then it will give up and move onto the next album
                        runs = 0
                        while(one_line_lyric_el != None and runs<30):
                            one_line_lyric = get_one_lyric(lyrics)
                            one_line_lyric_el = OneLineLyric.query(OneLineLyric.lyric_text==one_line_lyric and OneLineLyric.artist_key == artist_q_key and OneLineLyric.song_key == song_q_key).get()
                            runs = runs + 1
                        #if it finds a new one_line_lyric that isnt in the database before 30 runs:
                        # it puts in the databse
                        if runs<29:
                            new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=song_q_key,artist_key=artist_q_key)
                            new_one_line_lyric.put()
                            continue
                        else:
                            continue

        sleep(600)

        for album_name in album_dict2:
            sleep(2)
            logging.info("ALBUM NAME:")
            logging.info(album_name)
            artist_name = album_dict2[album_name]

            # This retrieves a random track from the selected album
            random_track = get_random_track(artist_name,album_name)
            if random_track == "Exception occurred \n":
                logging.info("EXCEPTION 1")
                logging.info(album_name)
                logging.info(artist_name)
                continue
            logging.info("RANDOM TRACK:")
            logging.info(random_track)
            #retrieves a str of any featured artists on the song
            featured_artists_str = get_artists_fr_song(artist_name,random_track)
            if featured_artists_str == "Exception occurred \n123":
                logging.info("EXCEPTION 2")
                logging.info(album_name)
                logging.info(artist_name)
                logging.info(random_track)
                continue

            # This retreives the entire lyrics of a song
            lyrics = get_lyrics(artist_name,random_track)
            # This randomly selects one line lyric from the song
            one_line_lyric = get_one_lyric(lyrics)
            logging.info("ONE LINE LYRIC:")
            logging.info(one_line_lyric)
            if one_line_lyric == "Exception occured \n123":
                logging.info("EXCEPTION 3")
                logging.info(album_name)
                logging.info(artist_name)
                continue

            #Now have to make sure that this lyric/song/artist combination isn't a duplicate
            artist_el = Artist.query(Artist.name == artist_name).get()
            #If this artist is not in the database at all:
            if artist_el == None:
                new_artist = Artist(name = artist_name)
                new_artist_key = new_artist.put()
                new_song = Song(title=random_track,artist_key=new_artist_key,feat_artist=featured_artists_str)
                new_song_key = new_song.put()
                new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=new_song_key,artist_key=new_artist_key)
                new_one_line_lyric.put()
                continue
            else:
                artist_q_key = artist_el.key
                song_el = Song.query(Song.title==random_track and Song.artist_key == artist_q_key and Song.feat_artist == featured_artists_str).get()
                #If this artist is in the database but the song is not:
                if song_el == None:
                    new_song = Song(title=random_track,artist_key=artist_q_key,feat_artist=featured_artists_str)
                    new_song_key = new_song.put()
                    new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=new_song_key,artist_key=artist_q_key)
                    new_one_line_lyric.put()
                    continue
                else:
                    song_q_key = song_el.key
                    one_line_lyric_el = OneLineLyric.query(OneLineLyric.lyric_text==one_line_lyric and OneLineLyric.artist_key == artist_q_key and OneLineLyric.song_key == song_q_key).get()
                    # if this artist and song are in the database but the one-line-lyric is not:
                    if one_line_lyric_el == None:
                        new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=song_q_key,artist_key=artist_q_key)
                        new_one_line_lyric.put()
                        continue
                    else:
                        #if this artist and song and this one_line_lyric_el are in the database:
                        # Then try to find a new one-line-lyric from that song that isn't in the database or
                        # After 30 tries, then it will give up and move onto the next album
                        runs = 0
                        while(one_line_lyric_el != None and runs<30):
                            one_line_lyric = get_one_lyric(lyrics)
                            one_line_lyric_el = OneLineLyric.query(OneLineLyric.lyric_text==one_line_lyric and OneLineLyric.artist_key == artist_q_key and OneLineLyric.song_key == song_q_key).get()
                            runs = runs + 1
                        #if it finds a new one_line_lyric that isnt in the database before 30 runs:
                        # it puts in the databse
                        if runs<29:
                            new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=song_q_key,artist_key=artist_q_key)
                            new_one_line_lyric.put()
                            continue
                        else:
                            continue

        sleep(600)

        for album_name in album_dict1:
            sleep(2)
            logging.info("ALBUM NAME:")
            logging.info(album_name)
            artist_name = album_dict1[album_name]

            # This retrieves a random track from the selected album
            random_track = get_random_track(artist_name,album_name)
            if random_track == "Exception occurred \n":
                logging.info("EXCEPTION 1")
                logging.info(album_name)
                logging.info(artist_name)
                continue
            logging.info("RANDOM TRACK:")
            logging.info(random_track)
            #retrieves a str of any featured artists on the song
            featured_artists_str = get_artists_fr_song(artist_name,random_track)
            if featured_artists_str == "Exception occurred \n123":
                logging.info("EXCEPTION 2")
                logging.info(album_name)
                logging.info(artist_name)
                logging.info(random_track)
                continue

            # This retreives the entire lyrics of a song
            lyrics = get_lyrics(artist_name,random_track)
            # This randomly selects one line lyric from the song
            one_line_lyric = get_one_lyric(lyrics)
            logging.info("ONE LINE LYRIC:")
            logging.info(one_line_lyric)
            if one_line_lyric == "Exception occured \n123":
                logging.info("EXCEPTION 3")
                logging.info(album_name)
                logging.info(artist_name)
                continue

            #Now have to make sure that this lyric/song/artist combination isn't a duplicate
            artist_el = Artist.query(Artist.name == artist_name).get()
            #If this artist is not in the database at all:
            if artist_el == None:
                new_artist = Artist(name = artist_name)
                new_artist_key = new_artist.put()
                new_song = Song(title=random_track,artist_key=new_artist_key,feat_artist=featured_artists_str)
                new_song_key = new_song.put()
                new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=new_song_key,artist_key=new_artist_key)
                new_one_line_lyric.put()
                continue
            else:
                artist_q_key = artist_el.key
                song_el = Song.query(Song.title==random_track and Song.artist_key == artist_q_key and Song.feat_artist == featured_artists_str).get()
                #If this artist is in the database but the song is not:
                if song_el == None:
                    new_song = Song(title=random_track,artist_key=artist_q_key,feat_artist=featured_artists_str)
                    new_song_key = new_song.put()
                    new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=new_song_key,artist_key=artist_q_key)
                    new_one_line_lyric.put()
                    continue
                else:
                    song_q_key = song_el.key
                    one_line_lyric_el = OneLineLyric.query(OneLineLyric.lyric_text==one_line_lyric and OneLineLyric.artist_key == artist_q_key and OneLineLyric.song_key == song_q_key).get()
                    # if this artist and song are in the database but the one-line-lyric is not:
                    if one_line_lyric_el == None:
                        new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=song_q_key,artist_key=artist_q_key)
                        new_one_line_lyric.put()
                        continue
                    else:
                        #if this artist and song and this one_line_lyric_el are in the database:
                        # Then try to find a new one-line-lyric from that song that isn't in the database or
                        # After 30 tries, then it will give up and move onto the next album
                        runs = 0
                        while(one_line_lyric_el != None and runs<30):
                            one_line_lyric = get_one_lyric(lyrics)
                            one_line_lyric_el = OneLineLyric.query(OneLineLyric.lyric_text==one_line_lyric and OneLineLyric.artist_key == artist_q_key and OneLineLyric.song_key == song_q_key).get()
                            runs = runs + 1
                        #if it finds a new one_line_lyric that isnt in the database before 30 runs:
                        # it puts in the databse
                        if runs<29:
                            new_one_line_lyric = OneLineLyric(lyric_text=one_line_lyric,vote_count=0,song_key=song_q_key,artist_key=artist_q_key)
                            new_one_line_lyric.put()
                            continue
                        else:
                            continue

            # at this point, a new one-line-lyric element has been added to the database, and there is a song and an artist
            # in the databse UNLESS every one-line-lyric element from a specific song has already been added to the databse





app = webapp2.WSGIApplication([
    ('/crons/oneline',OneLineHandler)
], debug=True)
