# ETL Spotify and Songkick
## Description
Uses the Spotify and Songkick APIs to favorite tracks and information about their upcoming shows. This information is stored into a MySQL database.

## Extract
### Spotify
Uses the spotipy module. Pulls the user's 50 favorite tracks in the json format found here: [link](https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/). 
### Songkick
Pulls from SongKick's Artist and Events APIs:
#### Find an Artist:
- https://api.songkick.com/api/3.0/search/artists.json?apikey={your_api_key}&query={artist_name}
```javascript
  {
    "resultsPage": {
      "results": {
        "artist": [
          {
            "id":253846,
            "uri":"http://www.songkick.com/artists/253846-radiohead",
            "displayName":"Radiohead",
            "onTourUntil":"2010-01-01"
          }
        ]
      },
      "totalEntries":1,
      "perPage":50,
      "page":1,
      "status":"ok"
    }
  }
 ```

#### Find an Event: 
- https://api.songkick.com/api/3.0/events/{event_id}.json?apikey={your_api_key}
    
```javascript
{
    "resultsPage": {
      "results": {
        "event": {
          "location": { "city":"London, UK", "lng":-0.1150322, "lat":51.4650846 },
          "popularity":0.526304,
          "uri":"http://www.songkick.com/concerts/3037536-vampire-weekend-at-o2-academy-brixton?utm_source=PARTNER_ID&utm_medium=partner",
          "displayName":"Vampire Weekend with Fan Death at O2 Academy Brixton (February 16, 2010)",
          "id":3037536,
          "type":"Concert",
          "start": { "time":"19:30:00", "date":"2010-02-16", "datetime":"2010-02-16T19:30:00+0000" },
          "ageRestriction": "14+",
          "performance":[
            {
              "artist": {
                "uri":"http://www.songkick.com/artists/288696-vampire-weekend?utm_source=PARTNER_ID&utm_medium=partner",
                "displayName":"Vampire Weekend",
                "id":288696,
                "identifier":[ { "href":"http://api.songkick.com/api/3.0/artists/mbid:af37c51c-0790-4a29-b995-456f98a6b8c9.json","mbid":"af37c51c-0790-4a29-b995-456f98a6b8c9" } ]
              },
              "displayName":"Vampire Weekend",
              "billingIndex":1,
              "id":5380281,
              "billing":"headline"
            },
            {
              "artist": {
                "uri":"http://www.songkick.com/artists/2357033-fan-death?utm_source=PARTNER_ID&utm_medium=partner",
                "displayName":"Fan Death",
                "id":2357033,
                "identifier": [ { "href":"http://api.songkick.com/api/3.0/artists/mbid:2ec79a0d-8b5d-4db2-ad6b-e91b90499e87.json","mbid":"2ec79a0d-8b5d-4db2-ad6b-e91b90499e87" } ]
              },
              "displayName":"Fan Death",
              "billingIndex":2,
              "id":7863371,
              "billing":
              "support"
            }
          ],
          "venue": {
            "metroArea": {
              "uri":"http://www.songkick.com/metro_areas/24426-uk-london?utm_source=PARTNER_ID&utm_medium=partner",
              "displayName":"London",
              "country": { "displayName":"UK" },
              "id":24426
            },
            "city": {
              "uri":"http://www.songkick.com/metro_areas/24426-uk-london?utm_source=PARTNER_ID&utm_medium=partner",
              "displayName":"London",
              "country": { "displayName":"UK" },
              "id":24426
             },
             "zip":"SW9 9SL",
             "lat":51.4650846,
             "lng":-0.1150322,
             "uri":"http://www.songkick.com/venues/17522-o2-academy-brixton?utm_source=PARTNER_ID&utm_medium=partner",
             "displayName":"O2 Academy Brixton",
             "street":"211 Stockwell Road",
             "id":17522,
             "website":"http://www.brixton-academy.co.uk/",
             "phone":"020 7771 3000",
             "capacity":4921,
             "description":"Brixton Academy is an award winning music venue situated in the heart of Brixton, South London. The venue has played host to many notable shows and reunions, welcoming a wide variety of artists, from Bob Dylan to Eminem, to the stage. It attracts over half a million visitors per year, accommodating over one hundred events.\n\nBuilt in 1929, the site started life as one of the four state of the art\n Astoria Theaters, screening a variety of motion pictures and shows. In 1972 the venue was transformed into a rock venue and re-branded as The Sundown Centre. With limited success the venue closed it’s doors in 1974 and was not re-opened as a music venue again until 1983, when it became The Brixton Academy.\n\nFeaturing a beautiful Art Deco interior, the venue is now known as the 02 Academy Brixton, and hosts a diverse range of club nights and live performances, as well as seated events. The venue has an upstairs balcony as well as the main floor downstairs. There is disabled access and facilities, a bar and a cloakroom. Club night events are for over 18s, for live music under 14s must be accompanied by an adult."
          },
          "status":"ok"
        }
      },
      "status":"ok"
    }
  }
  ```

## Transform
Using SQLAlchemy the Spotify data is loaded into the database.

### Spotify
#### Artist Class:
```python
class Artist(Base):
    __tablename__ = 'artists'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    songkick_id = Column(Integer, unique=True)

    albums = relationship('Album', backref='artist')
    tracks = relationship('Track', backref='artist')
    events = relationship('Event', backref='artist')

    def __repr__(self):
        return f'<Artist (id= {self.id}, ' \
            f'name={self.name}, songkick_id={self.songkick_id}, ' \
            f'albums={self.albums}, tracks={self.tracks}'
```
#### Album Class
```
class Album(Base):
    __tablename__ = 'albums'

    id = Column(String(50), primary_key=True)
    title = Column(String(150))
    artist_id = Column(String(50), ForeignKey('artists.id'))

    tracks = relationship('Track', backref='album')

    def __repr__(self):
        return f'<Album (id={self.id}, title={self.title} ' \
            f'artist_id={self.artist_id}, artist={self.artist}>'
```
#### Track Class
```
class Track(Base):
    __tablename__ = 'tracks'

    id = Column(String(50), primary_key=True)
    title = Column(String(150))
    duration_ms = Column(Float)
    album_id = Column(String(50), ForeignKey('albums.id'))
    artist_id = Column(String(50), ForeignKey('artists.id'))

    def __repr__(self):
        return f'<Track id={self.id}, title={self.title} ' \
            f'album_id={self.album_id}>'
```

### Songkick
#### Venue Class
```
class Venue(Base):
    __tablename__ = 'venue'

    id = Column(Integer, primary_key=True)

    name = Column(String(150))
    city = Column(String(100))

    events = relationship('Event', backref='venue')

    def __repr__(self):
        return f'<Venue id={self.id}, name={self.name}, city={self.city}>'

#### Event Class
```
class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    songkick_artist_id = Column(Integer, ForeignKey('artists.songkick_id'))
    venue_id = Column(Integer, ForeignKey('venue.id'))

    def __repr__(self):
        return f'<Event id={self.id}, date={self.date}, ' \
            f'songkick_artist_id={self.songkick_artist_id}, venue_id={self.venue_id}>'
```
## Built With
- [SQLAlchemy](https://docs.sqlalchemy.org/en/13/core/engines.html)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy](https://spotipy.readthedocs.io/en/latest/)
- [Songkick](https://www.songkick.com/developer)
    
  

