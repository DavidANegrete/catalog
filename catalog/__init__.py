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
def logInDecorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if 'username' not in login_session:
            return redirect (url_for('showLogin', next = request.url))
        return f(*args, **kwds)
    return wrapper

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE = state)

# FB - loggin
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"

    # strip expire tag from access token
    token = result.split("&")[0]
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, 
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash('You are now signed in!')

    return render_template('pupshome.html')


@app.route("/")

def hello():
    return "Hello, I love Digital Ocean!"
if __name__ == "__main__":
    app.run()
