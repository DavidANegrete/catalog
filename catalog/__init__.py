from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


@app.route("/")

def hello():
    return "Hello, I love Digital Ocean!"
if __name__ == "__main__":
    app.run()
