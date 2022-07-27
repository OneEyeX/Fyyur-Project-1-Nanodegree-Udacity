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

#
import collections

collections.Callable = collections.abc.Callable

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
# to disable tracker msj
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

moment = Moment(app)
app.config.from_object("config")
# db = SQLAlchemy(app)

# TODO: connect to a local postgresql database (DONE)
db = db_config(app)

# db_config() located in models.py

migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


# show error messages
def form_errors_messages(form):
    for inputs, messages in form.errors.items():
        for message in messages:
            flash(message)


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


@app.route("/")
def index():
    # CHALLENGE 2: Show 10 Recent Listed (newly created) Artists and Recently Listed Venues on the homepage
    # ordering query by id descending by order_by(id.desc()) and limit(10) to get only 10 records
    latest_10_Venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
    latest_10_Artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
    return render_template(
        "pages/home.html",
        latest_10_Venues=latest_10_Venues,
        latest_10_Artists=latest_10_Artists,
    )

    # return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    # get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #  get all the venues grouped by venue id , state and city
    venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()

    # initialization of parameters
    venue_state_and_city = []
    data = []
    # loop through venues to check for upcoming shows, city, states and venue information
    if venues:
        for venue in venues:
            # determine upcoming shows (new shows) that the start time is greater than the current time
            # or the past shows (old shows) that the start time is lesser or equal to the current time
            all_shows = venue.shows.all()

            # initialization of dicts
            upcoming_shows = []
            past_shows = []

            for show in all_shows:

                # comparing show  start time with current time to
                # determine new and past shows
                if str(show.start_time) > current_time:
                    upcoming_shows.append(show)
                else:
                    past_shows.append(show)

            # upcoming_shows = venue.query.filter(
            #     Show.start_time > current_time).all()
            # print(len(upcoming_shows))

            # to set grouped list of venues grouped by state and city
            if venue.city + venue.state in venue_state_and_city:

                data[venue_state_and_city.index(venue.city + venue.state)][
                    "venues"
                ].append(
                    {
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": len(upcoming_shows),
                    }
                )
            else:
                venue_state_and_city.append(venue.city + venue.state)
                data.append(
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
        return render_template("pages/venues.html", areas=data)
    flash("There is no Venues")
    return render_template("errors/404.html")


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    venue_query = Venue.query.filter(
        Venue.name.ilike("%" + request.form["search_term"] + "%")
    )
    venue_list = list(map(Venue.name_and_id, venue_query))
    response = {"count": len(venue_list), "data": venue_list}
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/shows/search", methods=["POST", "GET"])
def search_shows():

    term = request.form.get("search_term")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    shows_query = (
        db.session.query(Show)
        .join(Artist)
        .join(Venue)
        .filter(
            (Artist.name.ilike("%" + str(term) + "%"))
            | (Venue.name.ilike("%" + str(term) + "%"))
            # | (Show.start_time.ilike("%" + str(term) + "%"))
        )
        .order_by(Show.start_time.desc())
    )
    #
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

    # shows = list(map(Show.all_details, shows_query))
    # print(len(shows))

    # if shows:

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
    # return render_template("pages/show.html", shows=shows)
    # return render_template("pages/shows.html", shows=shows)

    # flash("No result found ")
    # return render_template("errors/404.html")

    # return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


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
            Show.query.options(db.joinedload(Show.Venue))
            .filter(Show.venue_id == venue_id)
            .all()
        )
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

    # old data
    # data1 = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "past_shows": [{
    #         "artist_id": 4,
    #         "artist_name": "Guns N Petals",
    #         "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "genres": ["Classical", "R&B", "Hip-Hop"],
    #     "address": "335 Delancey Street",
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "914-003-1132",
    #     "website": "https://www.theduelingpianos.com",
    #     "facebook_link": "https://www.facebook.com/theduelingpianos",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #     "address": "34 Whiskey Moore Ave",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "415-000-1234",
    #     "website": "https://www.parksquarelivemusicandcoffee.com",
    #     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "past_shows": [{
    #         "artist_id": 5,
    #         "artist_name": "Matt Quevedo",
    #         "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [{
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 1,
    # }
    # data = list(filter(lambda d: d['id'] ==
    #             venue_id, [data1, data2, data3]))[0]
    # return render_template('pages/show_venue.html', venue=data)


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

    if form.validate_on_submit():
        new_venue = Venue()
        new_venue.name = request.form.get("name")
        new_venue.genres = request.form.getlist("genres")
        new_venue.address = request.form.get("address")
        new_venue.city = request.form.get("city")
        new_venue.state = request.form.get("state")
        new_venue.phone = request.form.get("phone")
        new_venue.website_link = request.form.get("website_link")
        new_venue.facebook_link = request.form.get("facebook_link")
        new_venue.image_link = request.form.get("image_link")
        new_venue.seeking_talent = request.form.get("seeking_talent") == "y"
        new_venue.seeking_description = request.form.get("seeking_description")

        try:
            Venue.add_to_db(new_venue)
            # on successful db insert, flash success
            flash("Venue " + request.form["name"] +
                  " was successfully listed!")
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
    # to show error messages
    form_errors_messages(form)
    return render_template("forms/new_venue.html", form=form)
    # return render_template("pages/home.html")


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
            flash("Error occurred while deleting Venue " +
                  venue_to_delete.name + " .")
        finally:
            db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage (DONE)
    # DONE: button delete created and added in the file show_venue.html
    return redirect(url_for("index"))


#  Artists
#  ----------------------------------------------------------------


@app.route("/artists")
def artists():

    # TODO: replace with real data returned from querying the database (DONE)

    artists = Artist.query.all()
    if artists:
        return render_template("pages/artists.html", artists=artists)
    # else show message
    flash("There is no Artists")
    return render_template("errors/404.html")

    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    artists_query = Artist.query.filter(
        Artist.name.ilike("%" + request.form["search_term"] + "%")
    )
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


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    artist = Artist.query.get(artist_id)

    if artist:
        artist_details = Artist.all_details(artist)
        # get the current system time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get all the shows that are related to the venue
        shows_query = (
            Show.query.options(db.joinedload(Show.Artist))
            .filter(Show.artist_id == artist_id)
            .all()
        )
        # or
        # shows_query = (
        #     db.session.query(Show).join(
        #         Artist).filter(Show.artist_id == artist_id).all()
        # )
        # or in SQL
        # SELECT * FROM artists JOIN shows ON artists.id = shows.artist_id WHERE artist_id=someID;
        if shows_query:
            # initialization of lists of upcoming shows (new_shows) and past shows (past_shows)
            new_shows_list = []
            past_shows_list = []
            #
            for show in shows_query:
                # comparing show time start with current time to
                # determine new and past shows
                if str(show.start_time) > current_time:
                    new_shows_list.append(Show.all_details(show))
                else:
                    past_shows_list.append(Show.all_details(show))

            #
            artist_details["upcoming_shows"] = new_shows_list
            artist_details["upcoming_shows_count"] = len(new_shows_list)

            artist_details["past_shows"] = past_shows_list
            artist_details["past_shows_count"] = len(past_shows_list)

        return render_template("pages/show_artist.html", artist=artist_details)
    # else show message
    flash("There is no Artist with ID: " + str(artist_id))
    return render_template("errors/404.html")


#  Update
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
    # same as
    # artist = {
    #     "id": artist_query.id,
    #     "name": artist_query.name,
    #     "genres": list(artist_query.genres),
    #     "city": artist_query.city,
    #     "state": artist_query.state,
    #     "phone": artist_query.phone,
    #     "website": artist_query.website,
    #     "facebook_link": artist_query.facebook_link,
    #     "seeking_venue": artist_query.seeking_venue,
    #     "seeking_description": artist_query.seeking_description,
    #     "image_link": artist_query.image_link,
    # }
    # print(Artist.all_details(artist))


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    form = ArtistForm(request.form)

    edit_artist = Artist.query.get(artist_id)
    if edit_artist:
        if form.validate_on_submit():
            edit_artist.name = request.form.get("name")
            edit_artist.city = request.form.get("city")
            edit_artist.state = request.form.get("state")
            edit_artist.genres = request.form.getlist("genres")
            edit_artist.phone = request.form.get("phone")
            edit_artist.seeking_venue = request.form.get(
                "seeking_venue") == "y"
            edit_artist.seeking_description = request.form.get(
                "seeking_description")
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
                flash("Artist " + edit_artist.name +
                      " was successfully updated!")
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
        if form.validate_on_submit():
            edit_venue.name = request.form.get("name")
            edit_venue.genres = request.form.getlist("genres")
            edit_venue.address = request.form.get("address")
            edit_venue.city = request.form.get("city")
            edit_venue.state = request.form.get("state")
            edit_venue.phone = request.form.get("phone")
            edit_venue.website_link = request.form.get("website_link")
            edit_venue.facebook_link = request.form.get("facebook_link")
            edit_venue.image_link = request.form.get("image_link")
            edit_venue.seeking_talent = request.form.get(
                "seeking_talent") == "y"
            edit_venue.seeking_description = request.form.get(
                "seeking_description")
            try:
                # migrate and update the database
                Venue.add_to_db(edit_venue)
                # on successful db update, flash success
                flash("Venue " + edit_venue.name +
                      " was successfully updated!")
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

    if form.validate_on_submit():
        new_artist = Artist()
        new_artist.name = request.form.get("name")
        new_artist.city = request.form.get("city")
        new_artist.state = request.form.get("state")
        new_artist.genres = request.form.getlist("genres")
        new_artist.phone = request.form.get("phone")
        new_artist.seeking_venue = request.form.get("seeking_venue") == "y"
        new_artist.seeking_description = request.form.get(
            "seeking_description")
        new_artist.facebook_link = request.form.get("facebook_link")
        # print(new_artist.facebook_link)
        new_artist.image_link = request.form.get("image_link")
        new_artist.website_link = request.form.get("website_link")
        # added for the challenge 1
        new_artist.available = True

        try:
            # to add Artist to database
            Artist.add_to_db(new_artist)

            # on successful db insert, flash success
            flash("Artist " + request.form["name"] +
                  " was successfully listed!")
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

    # return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows", methods=["GET"])
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.

    # querying the database
    # shows_query = (
    # Show.query.options(db.joinedload(Show.Venue), db.joinedload(Show.Artist))
    # .order_by(Show.id.desc())
    # .all()
    # )
    shows_query = (
        db.session.query(Show).join(Venue).join(
            Artist).order_by(Show.id.desc()).all()
    )
    # to get all details of the queried result (show_query) and return them in a list
    shows = list(map(Show.all_details, shows_query))

    if shows:
        return render_template("pages/shows.html", shows=shows)
    # render error template if there is no show
    flash("There is no Shows")
    return render_template("errors/404.html")


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
        artist = Artist.query.get(artist_id)
        venue = Venue.query.get(venue_id)

        error = False

        if not artist:
            error = True
            flash("Artist with ID: " + artist_id + " not found")

        if not venue:
            error = True
            flash("Venue with ID: " + venue_id + " not found")

        # CHallenge 1
        # check if the artist is available or has a programmed show in that day
        # start_time = request.form.get("start_time")
        # convert time to format Y-m-d H:M:S
        start_time = datetime.strptime(
            str(request.form.get("start_time")), "%Y-%m-%d %H:%M:%S"
        )
        shows_artist = Show.query.filter(
            Show.artist_id == artist_id, Show.start_time == start_time
        ).first()

        if shows_artist:
            error = True
            flash(
                "Artist with ID: "
                + str(artist.id)
                + " already have a schedule in that date, try another date "
            )

        if artist and not artist.available:
            error = True
            flash(
                "Artist with ID: " + str(artist.id) +
                " is not available for booking "
            )

        # if there are no inputs errors (error==True)
        if not error:
            new_show = Show()
            new_show.venue_id = request.form.get("venue_id")
            new_show.artist_id = request.form.get("artist_id")
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

    # display form errors
    form_errors_messages(form)
    return render_template("forms/new_show.html", form=form)

    # # return render_template('pages/home.html')
    # # for error in form:
    # # flash(error.errors)
    # # show errors message
    # for key, value in form.errors.items():
    #     for val in value:
    #         flash(val)
    # return render_template("forms/new_show.html", form=ShowForm(request.form))


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
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
