from sqlalchemy import create_engine, Column, String, Integer, Float, \
    ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.orm.session import sessionmaker

import os

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)

    albums = relationship('Album', backref='artist')
    tracks = relationship('Track', backref='artist')

    def __repr__(self):
        return f'<Artist (id= {self.id}, ' \
            f'name={self.name}, albums={self.albums}, tracks={self.tracks}'


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


db_password = os.environ['MYSQL_PASSWORD']
engine = create_engine(
    f'mysql+pymysql://root:{db_password}@localhost:3306/music_db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

