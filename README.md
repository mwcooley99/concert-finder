# ETL Spotify and Songkick
## Description
I used the Spotify and Songkick APIs to get my favorite tracks and get information about their upcoming shows. I created a MySQL database, transformed the data and loaded it into my db.

## Extract
### Spotify
For the Spotify API I used the spotipy module. I used the module to get my 50 most popular tracks. They came in the json format found here: [link](https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/). 
### Songkick
For the Songkick API I made requets for Artists and Events. The urls used can be found here:
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
The data came in json format so I had to traverse to find the data that I needed. In addition to that I needed to run the spotify queries first and load them into the database first so I could establish keys for my favorite artists.

I used SQLAlchemy as an ORM and a MySQL database.

### Spotify
I created Artist, Album, and Track models for the Spotify data.

Here's the Artist Class:
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
### Songkick
I created Venue and Event Classes to handle this data

## Load
I used a relational database. This seemed like the logical choice because known relationships between the data.

Using an ORM made the actual load process straightforward. The exception was the need to check before loading to avoid loading duplicate data. For example, if I've already Added the Rolling Stones to the Artist Table, I don't want to add them again. I used the Spotify and Songkick ID's since I knew they would be unique and would make future API calls simple in the future.
 


    
  

