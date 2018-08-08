from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()


movies_genres_association = Table(
    'movies_genres', Base.metadata,
    Column('movie_id', Integer, ForeignKey('Movies.id')),
    Column('genre_id', Integer, ForeignKey('Genres.id'))
)


class Movie(Base):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    year = Column(Integer)
    country_id = Column(Integer, ForeignKey('Countries.id'))
    country = relationship("Country")
    genre = relationship(
        "Genre",
        secondary=movies_genres_association)

    def __init__(self, title, year, country):
        self.title = title
        self.year = year
        self.country = country


class Genre(Base):
    __tablename__ = 'Genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    movie = relationship(
        "Movie",
        secondary=movies_genres_association)

    def __init__(self, name):
        self.name = name


class Country(Base):
    __tablename__ = 'Countries'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name
