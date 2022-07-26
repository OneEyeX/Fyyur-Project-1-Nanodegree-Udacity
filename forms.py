from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    ValidationError,
    DateField,
)
from wtforms.validators import (
    AnyOf,
    URL,
    Regexp,
    InputRequired,
    Optional,
    DataRequired,
)
import re


# choices boxes
states_choices = [
    ("AL", "AL"),
    ("AK", "AK"),
    ("AZ", "AZ"),
    ("AR", "AR"),
    ("CA", "CA"),
    ("CO", "CO"),
    ("CT", "CT"),
    ("DE", "DE"),
    ("DC", "DC"),
    ("FL", "FL"),
    ("GA", "GA"),
    ("HI", "HI"),
    ("ID", "ID"),
    ("IL", "IL"),
    ("IN", "IN"),
    ("IA", "IA"),
    ("KS", "KS"),
    ("KY", "KY"),
    ("LA", "LA"),
    ("ME", "ME"),
    ("MT", "MT"),
    ("NE", "NE"),
    ("NV", "NV"),
    ("NH", "NH"),
    ("NJ", "NJ"),
    ("NM", "NM"),
    ("NY", "NY"),
    ("NC", "NC"),
    ("ND", "ND"),
    ("OH", "OH"),
    ("OK", "OK"),
    ("OR", "OR"),
    ("MD", "MD"),
    ("MA", "MA"),
    ("MI", "MI"),
    ("MN", "MN"),
    ("MS", "MS"),
    ("MO", "MO"),
    ("PA", "PA"),
    ("RI", "RI"),
    ("SC", "SC"),
    ("SD", "SD"),
    ("TN", "TN"),
    ("TX", "TX"),
    ("UT", "UT"),
    ("VT", "VT"),
    ("VA", "VA"),
    ("WA", "WA"),
    ("WV", "WV"),
    ("WI", "WI"),
    ("WY", "WY"),
]

genres_choices = [
    ("Alternative", "Alternative"),
    ("Blues", "Blues"),
    ("Classical", "Classical"),
    ("Country", "Country"),
    ("Electronic", "Electronic"),
    ("Folk", "Folk"),
    ("Funk", "Funk"),
    ("Hip-Hop", "Hip-Hop"),
    ("Heavy Metal", "Heavy Metal"),
    ("Instrumental", "Instrumental"),
    ("Jazz", "Jazz"),
    ("Musical Theatre", "Musical Theatre"),
    ("Pop", "Pop"),
    ("Punk", "Punk"),
    ("R&B", "R&B"),
    ("Reggae", "Reggae"),
    ("Rock n Roll", "Rock n Roll"),
    ("Soul", "Soul"),
    ("Other", "Other"),
]


def get_list_values(list):
    """
    a function that gets choices values
    for example for ("choice", "value")
    it return a list ["value",.. ]

    #### exapmle
    l=[("example1", "val1"), ("example2", "val2"), ("example3", "val3") ]
    get_list_values(l) return ["val1", "val2", "val3"]
    """

    values_list = []
    # loop through the items of the given list
    for items in list:
        # append each item's values to list value_list
        values_list.append(items[1])
    return values_list


# ----------------------------------------------------------------------------#
# Forms.
# ----------------------------------------------------------------------------#

#  ----------------------------------------------------------------
#  Show Form
#  ----------------------------------------------------------------
class ShowForm(FlaskForm):

    artist_id = StringField(
        "artist_id",
        validators=[
            InputRequired(message="Artist ID field is required"),
            Regexp(r"^\d", message="Artist ID field must be numeric"),
            # Regexp from Validators is used to make sure that the artist ID field is numeric
            # \d same as [0-9]
        ],
    )
    venue_id = StringField(
        "venue_id",
        validators=[
            InputRequired(message="Venue ID field is required"),
            Regexp(r"^\d", message="Venue ID field must be numeric"),
            # Regexp from Validators is used to make sure that the venue ID field is numeric
        ],
    )
    start_time = DateTimeField(
        "start_time",
        validators=[
            InputRequired(message="Date and time field is required"),
        ],
        default=datetime.today(),
    )

    # customized validators
    def validate_start_time(form, start_time):
        """
        a Custom validation for checking date format ( YYYY-MM-DD HH:MM:SS ) using regular expression
        """
        if not re.search(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", str(start_time)
        ):
            raise ValidationError("Date format must be YYYY-MM-DD HH:MM:SS")


#  ----------------------------------------------------------------
#  Venue Form
#  ----------------------------------------------------------------
class VenueForm(FlaskForm):

    name = StringField(
        "name",
        validators=[
            InputRequired(message="Name field is required"),
        ],
    )
    city = StringField(
        "city", validators=[InputRequired(message="City field is required")]
    )
    state = SelectField(
        "state",
        choices=states_choices,
        validators=[
            InputRequired(message="State Select field is required"),
            AnyOf(
                values=get_list_values(states_choices), message="Invalid State choice"
            ),
        ],
    )
    address = StringField(
        "address", validators=[InputRequired(message="Address field is required")]
    )
    phone = StringField(
        "phone",
        validators=[
            InputRequired(message="Phone field is required"),
            Regexp(
                r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$",
                message="Phone number is not valid, phone format must be xxx-xxx-xxxx",
            ),
            # Regexp from Validators is used to match phone number pattern which is xxx-xxx-xxxx
            # all x must be numbers
        ],
    )
    image_link = StringField(
        "image_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Image URL"),
        ],
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        "genres",
        validators=[
            InputRequired(message="Genres Select field is required"),
        ],
        choices=genres_choices,
    )
    facebook_link = StringField(
        "facebook_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Facebook URL"),
        ],
    )
    website_link = StringField(
        "website_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Website URL"),
        ],
    )

    seeking_talent = BooleanField("seeking_talent", default=False)

    seeking_description = StringField(
        "seeking_description",
        validators=[
            Optional(strip_whitespace=False),
            Regexp(r"^\w", message="Description field must be alphanumeric"),
            # Regexp from Validators is used to make sure that the description field is alphanumeric
            # \w same as [A-Z a-z 0-9]
        ],
    )


#  ----------------------------------------------------------------
#  Artist Form
#  ----------------------------------------------------------------
class ArtistForm(FlaskForm):
    name = StringField("name", validators=[InputRequired("Name field is required")])
    city = StringField("city", validators=[InputRequired("City field is required")])
    state = SelectField(
        "state",
        validators=[InputRequired("Select State field is required")],
        choices=states_choices,
    )
    phone = StringField(
        # TODO implement validation logic for phone
        "phone",
        validators=[
            InputRequired("Phone field is required"),
            Regexp(
                r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$",
                message="Phone number is not valid, phone format must be xxx-xxx-xxxx",
            ),
            # Regexp from Validators is used to match phone number pattern which is xxx-xxx-xxxx
            # all x must be numbers
        ],
    )
    genres = SelectMultipleField(
        "genres",
        validators=[
            InputRequired("Select Genres field is required"),
        ],
        choices=genres_choices,
    )
    image_link = StringField(
        "image_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Image URL"),
        ],
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        "facebook_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Facebook URL"),
        ],
    )

    website_link = StringField(
        "website_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Website URL"),
        ],
    )

    seeking_venue = BooleanField("seeking_venue", default=False)

    seeking_description = StringField(
        "seeking_description",
        validators=[
            Optional(strip_whitespace=False),
            Regexp(r"^\w", message="Description field must be alphanumeric"),
            # Regexp from Validators is used to make sure that the description is alphanumeric
            #  \w same as [A-Z a-z 0-9]
        ],
    )

    # added for CHALLENGE 1 : availability, so that an artist is only available to be booked at certain dates/times. Disable the ability to create book an artist for a show outside of their availability.
    available = BooleanField("available", default=False)


# added for the challenge
class SongForm(FlaskForm):

    song_name = StringField(
        "song_name",
        validators=[
            InputRequired(message="Song Name field is required"),
            Regexp(r"^\w", message="Song Name field must be alphanumeric"),
            # Regexp from Validators is used to make sure that the song name is alphanumeric
        ],
    )
    album_name = StringField(
        "album_name",
        validators=[
            Optional(strip_whitespace=False),
            Regexp(r"^\w", message="Album Name field must be alphanumeric"),
            # Regexp from Validators is used to make sure that the album name is alphanumeric
        ],
    )
    song_duration = StringField(
        "song_duration",
        validators=[
            InputRequired(message="Duration field is required"),
            Regexp(r"^\d", message="Duration field must be numeric"),
            # Regexp from Validators is used to make sure that the song duration is numeric
            # \d same as [0-9]+
        ],
    )
    song_link = StringField(
        "song_link",
        validators=[
            Optional(strip_whitespace=False),
            URL(message="Invalid Song URL"),
        ],
    )

    release_date = DateField(
        "release_date",
        validators=[
            InputRequired(message="Release date field is required"),
        ],
        default=datetime.today(),
    )

    # a custom validation logic for release_date:
    def validate_release_date(form, release_date):
        """
        a Custom validation for checking date format
        """
        if not re.search(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", str(release_date)
        ) and not re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", str(release_date)):
            raise ValidationError(
                "Date format must be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"
            )
