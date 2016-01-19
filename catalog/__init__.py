from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker


from flask import session as login_session
from werkzeug import secure_filename
from functools import wraps
import os
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
#from pup_methods import *
import logging

# Constants for uploads
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

# setting up the upload folder for the images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cross check Authentication
#CLIENT_ID = json.loads(
 #   open('client_secrets.json', 'r').read())['web']['client_id']
#APPLICATION_NAME = "Pups in the City"

# Connect to the Database and session
#engine = create_engine('sqlite:///puppyshelterwithusers.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind = engine)
#session = DBSession()

#pupQuery = session.query(Puppy)
#shelterQuery = session.query(Shelter)
#userQuery = session.query(User)
#queryPupnShelter = session.query(Puppy, Shelter)

# Decorator function to keep views accisible by some only.


@app.route('/')
@app.route('/pups/')
def pups():
    return render_template('pupshome.html')


if __name__ == "__main__":
    app.run()
