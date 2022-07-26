from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import (
    AnyOf,
    URL,
    Regexp,
    InputRequired,
    Optional,
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
    l = []
    for items in list:
        # for item in items:
        l.append(items[1])
    return l


# print(det(states_choices), len(det(states_choices)))
# print(get_list_values(genres_choices), len(get_list_values(genres_choices)))


class ShowForm(FlaskForm):

    artist_id = StringField(
        "artist_id",
        validators=[
            InputRequired(message="Artist ID field is required"),
            Regexp(r"^\d", message="Artist ID field must be numeric"),
        ],
    )
    venue_id = StringField(
        "venue_id",
        validators=[
            InputRequired(message="Venue ID field is required"),
            Regexp(r"^\d", message="Venue ID field must be numeric"),
        ],
    )
    start_time = DateTimeField(
        "start_time",
        validators=[
            InputRequired(message="Date and time field is required"),
        ],
        default=datetime.today(),
    )

    def validate_start_time(form, start_time):
        if not re.search(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", str(start_time)
        ):
            raise ValidationError(
                "Invalid Date format. Date format must be YYYY-MM-DD HH:MM:SS"
            )


class VenueForm(FlaskForm):
    #

    name = StringField(
        "name", validators=[InputRequired(message="Name field is required")]
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
                r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", message="Phone number is not valid"
            ),
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
            # AnyOf(genres_choices, "Invalid choice"),
            # AnyOf(
            # values=get_list_values(genres_choices), message="Invalid Genres choice"
            # ),
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

    seeking_description = StringField("seeking_description")

    # def validate_genres(form, genres):
    # g = list(genres)
    # print(genres)
    # for item in get_list_values(genres_choices):
    # print(item)
    # if not item in str(genres):
    # raise ValidationError("Invalid Genres choice")
    # for genre in g:
    # print(genre)

    # if not str(genre) in get_list_values(genres_choices):
    # raise ValidationError("Invalid Genres choice")


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
        # used Regexp from Validators
        "phone",
        validators=[
            InputRequired("Phone field is required"),
            Regexp(
                r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", message="Phone number is not valid"
            ),
        ],
    )
    genres = SelectMultipleField(
        "genres",
        validators=[InputRequired("Select Genres field is required")],
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

    seeking_description = StringField("seeking_description")
    # added for CHALLENGE 1
    available = BooleanField("available", default=False)
