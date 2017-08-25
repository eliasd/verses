from google.appengine.ext import ndb

class OneLineLyric(ndb.Model):
    lyric = ndb.StringProperty()
    upvotes = ndb.IntegerProperty()
    song_key = ndb.KeyProperty(Song)
    artist_key = ndb.KeyProperty(Artist)
