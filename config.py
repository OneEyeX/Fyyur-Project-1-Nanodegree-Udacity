import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# Done in models.py file

# TODO IMPLEMENT DATABASE URL
# database connection configuration
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:oex@localhost:5432/fyyurDb"

# make sure to create the database and change the configuration to your own settings,
# the default settings are below, you need just to uncomment the line below and put you PostgreSQL user password instead of yourPassword
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:yourPassword@localhost:5432/postgres"
