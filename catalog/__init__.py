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
import psycopg2
import json
from flask import make_response
import requests
#from pup_methods import *
import logging



app = Flask(__name__)

# Connect to the Database and session
engine = psycopg2.connect("debname=puppyshelterwithusers")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"
if __name__ == "__main__":
    app.run()
