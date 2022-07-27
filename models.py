from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, String
from forms import *


db = SQLAlchemy()

# Database connection configs
def db_config(app):
    """
    A function to configure the database connection
    and connect to a local postgreSQL database
    """
    db.app = app
    db.init_app(app)
    return db


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

#  ----------------------------------------------------------------
#  Model Venue
#  ----------------------------------------------------------------
class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    genres = db.Column(ARRAY(String))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())

    # relationship Venue-Show
    shows = db.relationship(
        "Show", backref="Venue", cascade="all, delete", lazy="dynamic"
    )

    #  ----------------------------------------------------------------
    #  Methods
    #  ----------------------------------------------------------------

    def __repr__(self):
        return f"<Venue ID={self.id} name={self.name} >"

    def add_to_db(self):
        """
        A method that adds object Venue to database (database migrations) and commit the changes
        """
        db.session.add(self)
        db.session.commit()

    def all_details(self):
        """
        A method that gets Venue all details (informations)
        and return them in a dictionary
        """
        dictionary = {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "address": self.address,
            "phone": self.phone,
            "image_link": self.image_link,
            "facebook_link": self.facebook_link,
            "seeking_description": self.seeking_description,
            "website": self.website_link,
            "genres": self.genres,
            "shows": self.shows,
            "seeking_talent": self.seeking_talent,
        }
        return dictionary

    def name_and_id(self):
        """
        A method that gets the Venue name and ID
        and return them in a dictionary
        """
        dictionary = {
            "id": self.id,
            "name": self.name,
        }
        return dictionary


#  ----------------------------------------------------------------
#  Model Artist
#  ----------------------------------------------------------------
class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # missing fileds
    # https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.ARRAY
    genres = db.Column(ARRAY(String))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String())

    # CHALLENGE 1: to add availability
    available = db.Column(db.Boolean, default=True)

    # relationship Artist-Show
    shows = db.relationship(
        "Show", backref="Artist", cascade="all, delete", lazy="dynamic"
    )
    # relationship Artist-Songs
    songs = db.relationship(
        "Song", backref="Artist", cascade="all, delete", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Artist ID:{self.id} name:{self.name}>"

    def add_to_db(self):
        """
        A method that adds object Artist to database (database migrations) and commit the changes
        """
        db.session.add(self)
        db.session.commit()

    def all_details(self):
        """
        A method that gets artist all details (informations)
        and return them in a dictionary
        """
        dictionary = {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website_link,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
        }
        return dictionary

    def name_and_id(self):
        """
        A method that gets Artist name and ID
        and return them in a dictionary
        """
        dictionary = {
            "id": self.id,
            "name": self.name,
        }
        return dictionary


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#  ----------------------------------------------------------------
#  Model Show
#  ----------------------------------------------------------------
class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)

    # foreign key related to table Venue with CASCADE delete enabled (to ensure integrity)
    venue_id = db.Column(
        db.Integer, db.ForeignKey(Venue.id, ondelete="CASCADE"), nullable=True
    )

    # foreign key related to table Artist with CASCADE delete enabled (to ensure integrity)
    artist_id = db.Column(
        db.Integer, db.ForeignKey(Artist.id, ondelete="CASCADE"), nullable=True
    )

    #  ----------------------------------------------------------------
    #  Methods
    #  ----------------------------------------------------------------

    def __repr__(self):
        return (
            f"<Show ID={self.id} Venue_ID={self.venue_id} Artist_ID={self.artist_id} >"
        )

    def add_to_db(self):
        """
        A method that adds object Show to database (database migrations) and commit the changes
        """
        db.session.add(self)
        db.session.commit()

    def all_details(self):
        """
        A method that gets Show all details ( informations )
        and return them in a dictionary
        """
        dictionary = {
            "venue_id": self.venue_id,
            "venue_name": self.Venue.name,
            "artist_id": self.artist_id,
            "artist_name": self.Artist.name,
            "artist_image_link": self.Artist.image_link,
            "start_time": str(self.start_time),
        }
        return dictionary


#  ----------------------------------------------------------------
#  CHALLENGE 3 : Showcase what albums and songs an artist has on the Artist's page
#  ----------------------------------------------------------------
#  Model Song
#  ----------------------------------------------------------------
class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    album_name = db.Column(db.String(), nullable=True)
    link = db.Column(db.String(), nullable=True)

    # foreign key related to table Artist with CASCADE delete enabled (to ensure integrity)
    artist_id = db.Column(
        db.Integer, db.ForeignKey(Artist.id, ondelete="CASCADE"), nullable=True
    )

    #  ----------------------------------------------------------------
    #  Methods
    #  ----------------------------------------------------------------

    def __repr__(self):
        return f"<Song ID={self.id} name={self.name} duration={self.duration} release_date={self.release_date} >"

    def add_to_db(self):
        """
        A method that adds object Song to database (database migrations) and commit the changes
        """
        db.session.add(self)
        db.session.commit()

    def all_details(self):
        """
        A method that gets Song all details (informations)
        and return them in a dictionary
        """
        dictionary = {
            "song_id": self.id,
            "song_name": self.name,
            "album_name": self.album_name,
            "artist_id": self.artist_id,
            "artist_name": self.Artist.name,
            "artist_image_link": self.Artist.image_link,
            "release_date": str(self.release_date),
            "duration": str(self.duration),
            "link": str(self.link),
        }
        return dictionary
