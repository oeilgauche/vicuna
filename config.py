# -*- coding: utf-8 -*-

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Database migration options
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

# Application threads. A common general assumption is 
# using 2 par vailable processor cores - to handle
# incoming requests using one and performing background
# operations using the other
THREADS_PER_PAGE = 2

# Enable protection agains CSRF
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the date
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Available languages for Babel
LANGUAGES = {
	'en': 'English',
	'fr': 'Français'
}