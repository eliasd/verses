from google.appengine.ext import ndb

class OneLineLyric(ndb.Model):
    lyric = ndb.StringProperty()
    upvotes = ndb.IntegerProperty()
    song_key = ndb.KeyProperty(Song)
    artist_key = ndb.KeyProperty(Artist)

class Song(ndb.Model):
    title = ndb.StringProperty()
    artist_key = ndb.KeyPropery(Artist)

class Artist(ndb.Model):
    name = ndb.StringProperty()
