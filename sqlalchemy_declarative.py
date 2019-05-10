import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer, Float, \
    ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import os

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        print(f'<Artist (id= {self.id}, name={self.name}>')


class Album(Base):
    __tablename__ = 'albums'

    id = Column(String(50), primary_key=True)
    title = Column(String(50))
    artist_id = Column(String(50), ForeignKey('artists.id'))

    artist = relationship('Artist', back_populates='albums')

    def __repr__(self):
        print(
            f'<Album (id={self.id}, title={self.title}, '
            f'artist_id={self.artist_id}, artist={self.artist}>')


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(String(50), primary_key=True)
    title = Column(String(50))
    duration_ms = Column(Float)
    album_id = Column(String(50), ForeignKey('albums.id'))

    album = relationship('Album', back_populates='tracks')

    def __repr__(self):
        print(
            f'<Track (id={self.id}, title={self.title}, '
            f'album_id={self.album_id}, artist={self.album}>')


db_password = os.environ['MYSQL_PASSWORD']
engine = create_engine(
    f'mysql+pymysql://root:{db_password}@localhost:3306/music_db')

Base.metadata.create_all(engine)
