# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from models import *
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate

# Added to resolve the issue AttributeError 'collections' has no attribute 'Callable'
import collections

collections.Callable = collections.abc.Callable

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
# to disable sqlAlchemy tracker error message
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

moment = Moment(app)
app.config.from_object("config")

# TODO: connect to a local postgresql database (DONE)
db = db_config(app)

# db_config() located in models.py

migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def form_errors_messages(form):
    """
    A custom function to display and show form's error messages
    """
    # loop through each field in the form to get the fields and the error messages and put them in a different lists
    # list(input_fields) for form fields and list(field_errors) for field errors
    for input_field, field_errors in form.errors.items():
        # loop through each field errors list and display the error
        for error in field_errors:
            flash(error)


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

#  ----------------------------------------------------------------
#  Home page
#  ----------------------------------------------------------------
@app.route("/")
def index():

    # CHALLENGE 2: Show Recent Listed Artists and Recently Listed Venues on the homepage,
    # returning results for Artists and Venues sorting by newly created.
    # Limit to the 10 most recently listed items.

    # ordering query by id descending by order_by(id.desc()) and limit(10) to get only 10 records
    latest_10_Venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
    latest_10_Artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()

    # in raw SQL:
    """
    SELECT * 
    FROM venues 
    ORDER BY venues.id DESC
    LIMIT 10;

    SELECT * 
    FROM artists 
    ORDER BY artists.id DESC
    LIMIT 10;
    """

    return render_template(
        "pages/home.html",
        latest_10_Venues=latest_10_Venues,
        latest_10_Artists=latest_10_Artists,
    )


#  ----------------------------------------------------------------
#  All Venues
#  ----------------------------------------------------------------
@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    # get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #  get all the venues grouped by venue id , state and city
    venues = Venue.query.group_by(Venue.state, Venue.city, Venue.id).all()
    # in raw SQL:
    """
    SELECT * 
    FROM venues
    GROUP BY venue.state,venue.city,venues.id;
    """

    if venues:
        # initialization of parameters
        # add city and state to a list  to group venues state and city
        venue_state_and_city = []
        # final result that will be passed to the frontend
        final_results = []

        # loop through venues to check for upcoming shows, city, states and venue information
        for venue in venues:
            # get all shows of the venue
            all_shows = venue.shows.all()

            # initialization of dicts
            upcoming_shows = []
            past_shows = []

            # determine upcoming shows (new shows) that the start time is greater than the current time
            # or the past shows (old shows) that the start time is lesser or equal to the current time
            #  loop through all shows to determine upcoming shows and past shows
            for show in all_shows:
                # comparing show  start time with current time to
                # determine new and past shows
                if str(show.start_time) > current_time:
                    upcoming_shows.append(show)
                else:
                    past_shows.append(show)

            # to display venues grouped by state and city i used a hacky way , explained below
            # if the state and city exist in the venue_state_list
            # the venue will be added to data in the index of the state_and_city list
            if venue.city + " " + venue.state in venue_state_and_city:
                final_results[
                    venue_state_and_city.index(venue.city + " " + venue.state)
                ]["venues"].append(
                    {
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": len(upcoming_shows),
                    }
                )
            else:
                # if not the state and city will be added to the state_and_city list (to use it for testing later),
                venue_state_and_city.append(venue.city + " " + venue.state)
                # the city, the state and the venue will be added to the final result
                final_results.append(
                    {
                        "city": venue.city,
                        "state": venue.state,
                        "venues": [
                            {
                                "id": venue.id,
                                "name": venue.name,
                                "num_upcoming_shows": len(upcoming_shows),
                            }
                        ],
                    }
                )
        return render_template("pages/venues.html", areas=final_results)
    # if there are no venues
    flash("There is no Venues")
    return render_template("errors/404.html")


#  ----------------------------------------------------------------
#  Venue search
#  ----------------------------------------------------------------
@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    # get searched term
    term = request.form.get("search_term")

    # query the database
    venue_query = Venue.query.filter(Venue.name.ilike("%" + term + "%"))
    # ilike is used to make the search case insensitive
    # in raw SQL :
    """
    SELECT * 
    FROM venues 
    WHERE name ILIKE(search_term);
    """

    # to transform the query results into list
    venue_list = list(map(Venue.name_and_id, venue_query))

    # final result
    response = {
        "count": len(venue_list),
        "data": venue_list,
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


#  ----------------------------------------------------------------
#  Display Venue page with Venue's informations
#  ----------------------------------------------------------------
@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    # to get the venue with the given venue_id
    venue = Venue.query.get(venue_id)
    # if venue exists
    if venue:
        # get venue infos
        venue_dict = Venue.all_details(venue)

        # get current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get all the shows that are related to the venue
        shows_query = (
            db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).all()
        )
        # or also
        # shows_query = (
        #     Show.query.options(db.joinedload(Show.Venue))
        #     .filter(Show.venue_id == venue_id)
        #     .all()
        # )
        # in raw SQL:
        """
        SELECT * 
        FROM shows JOIN venues ON shows.venue_id = venues.id
        WHERE shows.venue_id= venue_id;
        """
        # if there are shows
        if shows_query:
            # initialization of lists of upcoming shows (new_shows) and past shows (past_shows)
            new_shows = []
            past_shows = []
            #
            for show in shows_query:
                # comparing show start time with current time to
                # determine new and past shows
                if str(show.start_time) > current_time:
                    new_shows.append(Show.all_details(show))
                else:
                    past_shows.append(Show.all_details(show))

            # adding data to venue dict to pass it to the frontend
            venue_dict["upcoming_shows"] = new_shows
            venue_dict["upcoming_shows_count"] = len(new_shows)
            venue_dict["past_shows"] = past_shows
            venue_dict["past_shows_count"] = len(past_shows)

        # render the template page with the queried data
        return render_template("pages/show_venue.html", venue=venue_dict)

    # (else) render error template in case of error
    flash("There is no Venue with ID: " + str(venue_id))
    return render_template("errors/404.html")


#  ----------------------------------------------------------------
#  Create Venue
#  ----------------------------------------------------------------
@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = VenueForm(request.form)

    # check if name or phone is already used
    name = request.form.get("name")
    phone = request.form.get("phone")
    query_name = Venue.query.filter(Venue.name == name).first()
    query_phone = Venue.query.filter(Venue.phone == phone).first()

    error = False
    if query_name:
        error = True
        flash("name already exists in database")
    if query_phone:
        error = True
        flash("phone already exists in database")

    if not error and form.validate_on_submit():
        new_venue = Venue()
        new_venue.name = name
        new_venue.genres = request.form.getlist("genres")
        new_venue.address = request.form.get("address")
        new_venue.city = request.form.get("city")
        new_venue.state = request.form.get("state")
        new_venue.phone = phone
        new_venue.website_link = request.form.get("website_link")
        new_venue.facebook_link = request.form.get("facebook_link")
        new_venue.image_link = request.form.get("image_link")
        new_venue.seeking_talent = request.form.get("seeking_talent") == "y"
        new_venue.seeking_description = request.form.get("seeking_description")
        print(new_venue.seeking_description)
        try:
            # add new venue to the database
            Venue.add_to_db(new_venue)
            # on successful db insert, flash success
            flash("Venue " + request.form["name"] + " was successfully listed!")
        except:
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            db.session.rollback()
            flash(
                "An error occurred. Venue "
                + request.form["name"]
                + " could not be listed."
            )
        finally:
            db.session.close()
            return redirect(url_for("index"))
    # to display form's error messages, this function is defined and explained in line 50
    form_errors_messages(form)
    return render_template("forms/new_venue.html", form=form)
    # return render_template("pages/home.html")


#  ----------------------------------------------------------------
#  Delete a Venue
#  ----------------------------------------------------------------
@app.route("/venues/<venue_id>/delete", methods=["GET", "DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # to get the venue to delete
    venue_to_delete = Venue.query.get(venue_id)

    if not venue_to_delete:
        flash("Venue not found.")
    else:
        try:
            db.session.delete(venue_to_delete)
            db.session.commit()
            flash("Venue " + venue_to_delete.name + " deleted successfully .")
        except:
            db.session.rollback()
            flash("Error occurred while deleting Venue " + venue_to_delete.name + " .")
        finally:
            db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage (DONE)
    # DONE: button delete created and added in the file show_venue.html
    return redirect(url_for("index"))


#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():

    # TODO: replace with real data returned from querying the database (DONE)

    # query the Database to get the list of artists
    # in SQL_Alchemy ORM:
    artists = Artist.query.all()

    # in raw SQL:
    """
    SELECT *
    FROM artists;
    """

    if artists:
        return render_template("pages/artists.html", artists=artists)

    # else show error message
    flash("There is no Artists")
    return render_template("errors/404.html")


#  ----------------------------------------------------------------
#  Artists Search
#  ----------------------------------------------------------------
@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    # get searched term
    term = request.form.get("search_term")

    # query the database
    # in SQL_Alchemy :
    artists_query = Artist.query.filter(Artist.name.ilike("%" + term + "%"))

    # in raw SQL:
    """
    SELECT *
    FROM artists
    WHERE artists.name ILIKE(searched_term)
    """

    # convert query to list
    artists_list = list(map(Artist.name_and_id, artists_query))

    results = {
        "count": len(artists_list),
        "data": artists_list,
    }
    return render_template(
        "pages/search_artists.html",
        results=results,
        search_term=request.form.get("search_term", ""),
    )


#  ----------------------------------------------------------------
#  Artist profile page
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    # Query the database
    # in SQL_Alchemy ORM:
    artist = Artist.query.get(artist_id)

    # in raw SQL:
    """
    SELECT *
    FROM artists
    WHERE id = artist_id;
    """

    if artist:
        # to get artist's all details and informations in a dictionary
        artist_details = Artist.all_details(artist)

        # get the current system time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get all the shows that are related to the venue

        # in SQL_Alchemy ORM:
        shows_query = (
            db.session.query(Show)
            .join(Artist)
            .filter(Show.artist_id == artist_id)
            .all()
        )
        # or also
        # shows_query = (
        #     Show.query.options(db.joinedload(Show.Artist))
        #     .filter(Show.artist_id == artist_id)
        #     .all()
        # )
        # in raw SQL:
        """
        SELECT * 
        FROM shows JOIN artists ON shows.artist_id= artists.id  
        WHERE artist_id=artist_id;
        """

        if shows_query:
            # initialization of lists of upcoming shows (new_shows) and past shows (past_shows)
            new_shows_list = []
            past_shows_list = []

            # loop through query results
            for show in shows_query:
                # comparing show time start with current time to
                # determine new and past shows
                if str(show.start_time) > current_time:
                    new_shows_list.append(Show.all_details(show))
                else:
                    past_shows_list.append(Show.all_details(show))

            # add new and past shows to the final list of results
            artist_details["upcoming_shows"] = new_shows_list
            artist_details["upcoming_shows_count"] = len(new_shows_list)
            artist_details["past_shows"] = past_shows_list
            artist_details["past_shows_count"] = len(past_shows_list)

        # Challenge 3 :Showcase what albums and songs an artist has on the Artist's page.
        songs_query = (
            db.session.query(Song)
            .join(Artist)
            .filter(Song.artist_id == artist_id)
            .order_by(Song.release_date.desc())
            .all()
        )
        # or also
        # songs_query = (
        #     Song.query.options(db.joinedload(Song.Artist))
        #     .filter(Song.artist_id == artist_id)
        #     .order_by(Song.release_date.desc())
        #     .all()
        # )
        # in raw SQL:
        """
        SELECT *
        FROM songs JOIN artists ON songs.artist_id = artists.id
        WHERE songs.artist_id= artist_id
        ORDER BY songs.release_date DESC;
        """
        if songs_query:
            # get the songs all details and informations in a list
            songs_list = list(map(Song.all_details, songs_query))

            # add the songs to the artist details dictionary
            artist_details["songs_count"] = len(songs_list)
            artist_details["songs"] = songs_list

        return render_template("pages/show_artist.html", artist=artist_details)
    # else show message
    flash("There is no Artist with ID: " + str(artist_id))
    return render_template("errors/404.html")


#  ----------------------------------------------------------------
#  Delete an Artist
#  (OPTION : it's not mentioned in the tasks list but I added it as a CHALLENGE)
#  ----------------------------------------------------------------
@app.route("/artists/<artist_id>/delete", methods=["GET", "DELETE"])
def delete_artist(artist_id):

    # to get the artist to delete
    artist_to_delete = Artist.query.get(artist_id)

    if not artist_to_delete:
        flash("Artist not found.")
    else:
        try:
            db.session.delete(artist_to_delete)
            db.session.commit()
            flash("Artist " + artist_to_delete.name + " deleted successfully .")
        except:
            db.session.rollback()
            flash(
                "Error occurred while deleting Artist " + artist_to_delete.name + " ."
            )
        finally:
            db.session.close()

    # clicking that button delete it from the db then redirect the user to the homepage (DONE)
    # DONE: button delete created and added in the file show_artists.html
    return redirect(url_for("index"))


#  ----------------------------------------------------------------
#  Update artist informations
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>

    artist = Artist.query.get(artist_id)
    if not artist:
        flash("Venue with ID : " + str(artist_id) + " not found")
        return redirect(url_for("index"))

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    form = ArtistForm(request.form)

    edit_artist = Artist.query.get(artist_id)
    if edit_artist:

        # check name and phone unicity
        name = request.form.get("name")
        phone = request.form.get("phone")
        query_name = Artist.query.filter(
            Artist.name == name, Artist.id != artist_id
        ).first()
        query_phone = Artist.query.filter(
            Artist.phone == phone, Artist.id != artist_id
        ).first()
        error = False
        if query_name:
            error = True
            flash("Name already exists in database, try another")
        if query_phone:
            error = True
            flash("Phone already exists in database, try another")

        if not error and form.validate_on_submit():
            edit_artist.name = name
            edit_artist.city = request.form.get("city")
            edit_artist.state = request.form.get("state")
            edit_artist.genres = request.form.getlist("genres")
            edit_artist.phone = phone
            edit_artist.seeking_venue = request.form.get("seeking_venue") == "y"
            edit_artist.seeking_description = request.form.get("seeking_description")
            edit_artist.facebook_link = request.form.get("facebook_link")
            edit_artist.image_link = request.form.get("image_link")
            edit_artist.website_link = request.form.get("website_link")
            # added for the challenge 1
            edit_artist.available = request.form.get("available") == "y"
            #
            try:
                # migrate and update the database
                Artist.add_to_db(edit_artist)
                # on successful db update, flash success
                flash("Artist " + edit_artist.name + " was successfully updated!")
            except:
                # TODO: on unsuccessful db insert, flash an error instead.
                # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
                db.session.rollback()
                flash(
                    "An error occurred. Artist "
                    + edit_artist.name
                    + " could not be updated."
                )
            finally:
                db.session.close()
                return redirect(url_for("show_artist", artist_id=artist_id))

        # display form errors
        form_errors_messages(form)
        return render_template("forms/edit_artist.html", form=form, artist=edit_artist)

    flash("Artist with ID: " + str(request.form.get("artist_id")) + ", not found")
    return redirect(url_for("index"))


#  ----------------------------------------------------------------
#  Update Venue informations
#  ----------------------------------------------------------------
@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()

    # TODO: populate form with values from venue with ID <venue_id>

    venue = Venue.query.get(venue_id)
    if not venue:
        flash("Venue with ID : " + str(venue_id) + " not found")
        return redirect(url_for("index"))

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    form = VenueForm(request.form)
    edit_venue = Venue.query.get(venue_id)
    if edit_venue:

        # check name and phone unicity
        name = request.form.get("name")
        phone = request.form.get("phone")
        query_name = Venue.query.filter(
            Venue.name == name, Venue.id != venue_id
        ).first()
        query_phone = Venue.query.filter(
            Venue.phone == phone, Venue.id != venue_id
        ).first()
        error = False
        if query_name:
            error = True
            flash("Name already exists in database, try another")
        if query_phone:
            error = True
            flash("Phone already exists in database, try another")

        if not error and form.validate_on_submit():
            edit_venue.name = name
            edit_venue.genres = request.form.getlist("genres")
            edit_venue.address = request.form.get("address")
            edit_venue.city = request.form.get("city")
            edit_venue.state = request.form.get("state")
            edit_venue.phone = phone
            edit_venue.website_link = request.form.get("website_link")
            edit_venue.facebook_link = request.form.get("facebook_link")
            edit_venue.image_link = request.form.get("image_link")
            edit_venue.seeking_talent = request.form.get("seeking_talent") == "y"
            edit_venue.seeking_description = request.form.get("seeking_description")
            try:
                # migrate and update the database
                Venue.add_to_db(edit_venue)
                # on successful db update, flash success
                flash("Venue " + edit_venue.name + " was successfully updated!")
            except:
                # rollback to the previous state
                db.session.rollback()
                # show an error message
                flash(
                    "An error occurred. Venue "
                    + edit_venue.name
                    + " could not be updated."
                )
            finally:
                # close the session
                db.session.close()
                return redirect(url_for("show_venue", venue_id=venue_id))

        # display form errors
        form_errors_messages(form)
        # return redirect(url_for("edit_venue_submission", venue_id=venue_id, form=form))
        return render_template("forms/edit_venue.html", form=form, venue=edit_venue)

    flash("Venue with ID : " + venue_id + "not found")
    return redirect(url_for("index"))
    # return render_template("forms/edit_venue.html", venue=venue_id, form=form)


#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------
@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = ArtistForm(request.form)
    name = request.form.get("name")
    phone = request.form.get("phone")
    query_name = Artist.query.filter(Artist.name == name).first()
    query_phone = Artist.query.filter(Artist.phone == phone).first()
    error = False
    if query_name:
        error = True
        flash("Name already exists in database, try another")
    if query_phone:
        error = True
        flash("Phone already exists in database, try another")

    if not error and form.validate_on_submit():
        new_artist = Artist()
        new_artist.name = name
        new_artist.city = request.form.get("city")
        new_artist.state = request.form.get("state")
        new_artist.genres = request.form.getlist("genres")
        new_artist.phone = phone
        new_artist.seeking_venue = request.form.get("seeking_venue") == "y"
        new_artist.seeking_description = request.form.get("seeking_description")
        new_artist.facebook_link = request.form.get("facebook_link")
        new_artist.image_link = request.form.get("image_link")
        new_artist.website_link = request.form.get("website_link")

        # added for the challenge 1
        # by default is True but it can be changed from edit artist
        new_artist.available = True

        try:
            # to add Artist to database
            Artist.add_to_db(new_artist)
            # on successful db insert, flash success
            flash("Artist " + new_artist.name + " was successfully listed!")
        except:
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
            db.session.rollback()
            flash(
                "An error occurred. Artist " + new_artist.name + " could not be listed."
            )
        finally:
            db.session.close()
        return redirect(url_for("index"))

    # display form errors
    form_errors_messages(form)
    return render_template("forms/new_artist.html", form=ArtistForm(request.form))


#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------
@app.route("/shows", methods=["GET"])
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.

    # querying the database
    shows_query = (
        db.session.query(Show).join(Venue, Artist).order_by(Show.id.desc()).all()
    )
    # or also
    # shows_query = Show.query.options(
    # db.joinedload(Show.Venue), db.joinedload(Show.Artist)
    # ).order_by(Show.id.desc()).all()
    # in raw SQL :
    """
    SELECT *
    FROM shows JOIN artists ON shows.artist_id= artists.id 
    JOIN venues ON shows.venue_id = venues.id 
    ORDER BY shows.id DESC;
    """

    # to get all details of the queried result (show_query) and return them in a list
    shows = list(map(Show.all_details, shows_query))

    if shows:
        # get the current time and pass it to the frontend to use it for personalizing
        # displayed message like if show time is lesser than current time the message will be played else it will be playing
        # check the shows template for more details ( pages/shows.html )
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template(
            "pages/shows.html", shows=shows, current_time=current_time
        )
    # render error template if there is no show
    flash("There is no Shows")
    return render_template("errors/404.html")


#  ----------------------------------------------------------------
#  Create a Show
#  ----------------------------------------------------------------
@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = ShowForm(request.form)

    if form.validate_on_submit():
        # check if artist id and venue id exist in the db
        artist_id = request.form.get("artist_id")
        venue_id = request.form.get("venue_id")

        # query the database
        artist = Artist.query.get(artist_id)
        venue = Venue.query.get(venue_id)

        # check if artist and venue exist
        error = False
        if not artist:
            error = True
            flash("Artist with ID: " + artist_id + " not found")

        if not venue:
            error = True
            flash("Venue with ID: " + venue_id + " not found")

        # CHallenge 1
        # check if the artist is available or has a programmed show in that day
        # get the start time from the form and convert it to format Y-m-d H:M:S
        start_time = datetime.strptime(
            str(request.form.get("start_time")), "%Y-%m-%d %H:%M:%S"
        )
        # query the database with SQL_Alchemy
        # to check if the artist already has a programmed show in that day
        shows_artist = Show.query.filter(
            Show.artist_id == artist_id, Show.start_time == start_time
        ).first()

        # in raw SQL :
        """
        SELECT * 
        FROM shows 
        WHERE shows.artist_id = artist_id 
        AND Show.start_time = start_time
        LIMIT 1;
        """

        # if artist has a programmed show in that day
        if shows_artist:
            error = True
            flash(
                "Artist with ID: "
                + str(artist.id)
                + " already has a schedule in that date, try another date "
            )

        # if artist is not available (the available checkbox is unchecked)
        if artist and not artist.available:
            error = True
            flash(
                "Artist with ID: " + str(artist.id) + " is not available for booking "
            )

        # if there are no inputs errors (error==True)
        if not error:
            new_show = Show()
            new_show.venue_id = venue_id
            new_show.artist_id = artist_id
            new_show.start_time = start_time

            try:
                Show.add_to_db(new_show)
                # on successful db insert, flash success
                flash("Show was successfully listed!")
            except:
                # TODO: on unsuccessful db insert, flash an error instead.
                db.session.rollback()
                flash("An error occurred. Show could not be listed.")
            finally:
                db.session.close()
                # e.g., flash('An error occurred. Show could not be listed.')
                # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
                return redirect(url_for("index"))

    # go back to add new show page and display form errors in order to inform the user what errors
    form_errors_messages(form)
    return render_template("forms/new_show.html", form=form)


#  ----------------------------------------------------------------
#  Show search
#  ----------------------------------------------------------------
@app.route("/shows/search", methods=["POST", "GET"])
def search_shows():

    term = request.form.get("search_term")

    # query the database
    # in SQL_Alchemy:
    shows_query = (
        db.session.query(Show)
        .join(Artist)
        .join(Venue)
        .filter(
            (Artist.name.ilike("%" + str(term) + "%"))
            | (Venue.name.ilike("%" + str(term) + "%"))
            # uncomment the line below to add search by date
            # | (Show.start_time.ilike("%" + str(term) + "%"))
        )
        .order_by(Show.start_time.desc())
    )

    # in raw SQL :
    """ 
    SELECT *
    FROM show JOIN artist on show.artist_id=artist.id 
    JOIN venues ON shows.venue_id=venues.id
    WHERE artist.name ILIKE(searched_term) and venues.name ILIKE(searched_term)
    ORDER BY show.start_time DESC;
    """

    past_shows = []
    new_shows = []
    # if there are shows
    # divide shows in new and past shows lists
    if shows_query:
        # get the current time in the format YYYY-MM-DD HH:MM:SS
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # loop through the show query to determine new shows and past shows
        for show in shows_query:
            # comparing show start time with current time to
            # determine new and past shows
            if str(show.start_time) > current_time:
                new_shows.append(Show.all_details(show))
            else:
                past_shows.append(Show.all_details(show))

    results = {
        "count": len(past_shows + new_shows),
        "past_shows_count": len(past_shows),
        "past_shows": past_shows,
        "new_shows_count": len(new_shows),
        "new_shows": new_shows,
    }

    flash("number of results " + str(len(past_shows + new_shows)) + " shows")
    return render_template(
        "pages/show.html",
        shows=results,
        search_term=request.form.get("search_term"),
    )


#  ----------------------------------------------------------------
#  CHALLENGE 3 : Showcase what albums and songs an artist has on the Artist's page
#  ----------------------------------------------------------------
#  ----------------------------------------------------------------
#  Create a Song
#  ----------------------------------------------------------------
@app.route("/artist/<artist_id>/song/create", methods=["POST", "GET"])
def create_song(artist_id):
    form = SongForm(request.form)
    artist = Artist.query.get(artist_id)
    if not artist:
        flash("Artist with ID: " + artist_id + " not found")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        new_song = Song()
        new_song.artist_id = artist_id
        new_song.name = request.form.get("song_name")
        new_song.album_name = request.form.get("album_name")
        new_song.duration = request.form.get("song_duration")
        new_song.link = request.form.get("song_link")
        new_song.release_date = request.form.get("release_date")

        try:
            Song.add_to_db(new_song)
            flash("Song " + new_song.name + "was successfully listed!")
        except:
            db.session.rollback()
            flash("An error occurred. Song could not be listed.")
        finally:
            db.session.close()
            return redirect(url_for("show_artist", artist_id=artist_id))

    # go back to add song page add and display form errors in order to inform the user what errors
    form_errors_messages(form)
    return render_template("forms/new_song.html", form=form)


#  ----------------------------------------------------------------
#  Delete a Song
#  OPTION : it's not mentioned in the list of tasks to do
#  I added it personally as an improvement for the website app
#  ----------------------------------------------------------------
@app.route("/song/<song_id>/delete", methods=["GET", "DELETE"])
def delete_song(song_id):
    # to get the song to delete
    song_to_delete = Song.query.get(song_id)

    if not song_to_delete:
        flash("Song not found.")
    else:
        try:
            db.session.delete(song_to_delete)
            db.session.commit()
            flash("Song " + song_to_delete.name + " deleted successfully .")
        except:
            db.session.rollback()
            flash("Error occurred while deleting Song " + song_to_delete.name + " .")
        finally:
            db.session.close()
    return redirect(url_for("show_artist", artist_id=song_to_delete.artist_id))


#  ----------------------------------------------------------------
#  Delete a Show
#  OPTION : it's not mentioned in the list of tasks to do
#  I added it personally as an improvement for the website app
#  ----------------------------------------------------------------
@app.route("/show/<show_id>/delete", methods=["GET", "DELETE"])
def delete_show(show_id):
    # to get the show to delete
    show_to_delete = Show.query.get(show_id)

    if not show_to_delete:
        flash("Show not found.")
    else:
        try:
            db.session.delete(show_to_delete)
            db.session.commit()
            flash("Show deleted successfully.")
        except:
            db.session.rollback()
            flash("Error occurred while deleting the Show.")
        finally:
            db.session.close()
    return redirect(url_for("shows"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
