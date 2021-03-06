# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
frontend = Blueprint('frontend', __name__)

# Set the route and accepted methods
@frontend.route('/')
def frontend_index():
    return render_template("frontend/index.html",
                            title='Home')