from sqlalchemy import create_engine, Column, String, Integer, Float, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.orm.session import sessionmaker

import os

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    songkick_id = Column(Integer)

    albums = relationship('Album', backref='artist')
    tracks = relationship('Track', backref='artist')
    events = relationship('Event', backref='artist')

    def __repr__(self):
        return f'<Artist (id= {self.id}, ' \
            f'name={self.name}, songkick_id={self.songkick_id}, ' \
            f'albums={self.albums}, tracks={self.tracks}'


class Album(Base):
    __tablename__ = 'albums'

    id = Column(String(50), primary_key=True)
    title = Column(String(150))
    artist_id = Column(String(50), ForeignKey('artists.id'))

    tracks = relationship('Track', backref='album')

    def __repr__(self):
        return f'<Album (id={self.id}, title={self.title} ' \
            f'artist_id={self.artist_id}, artist={self.artist}>'


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


class Venue(Base):
    __tablename__ = 'venue'

    id = Column(Integer, primary_key=True)

    name = Column(String(150))
    venue = Column(String(150))
    city = Column(String(100))

    events = relationship('Event', backref='venue')


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    songkick_artist_id = Column(Integer, ForeignKey('artists.songkick_id'))
    venue_id = Column(Integer, ForeignKey('venue.id'))

    def __repr__(self):
        return f'<Event id={self.id}, date={self.date}, ' \
            f'songkick_artist_id={self.songkick_artist_id}, venue_id={self.venue_id}'


def get_engine():
    db_password = os.environ['MYSQL_PASSWORD']
    return create_engine(
        f'mysql+pymysql://root:{db_password}@localhost:3306/music_db')


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    return Session()


if __name__ == '__main__':
    engine = get_engine()

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print(session.query(Artist).first())
