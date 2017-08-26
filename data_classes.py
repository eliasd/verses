from google.appengine.ext import ndb


class Artist(ndb.Model):
    name = ndb.StringProperty()

class Song(ndb.Model):
    title = ndb.StringProperty()
    artist_key = ndb.KeyProperty(Artist)

class OneLineLyric(ndb.Model):
    lyric_text = ndb.StringProperty()
    upvotes = ndb.IntegerProperty()
    song_key = ndb.KeyProperty(Song)
    artist_key = ndb.KeyProperty(Artist)
