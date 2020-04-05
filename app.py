from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from scripts import parser
# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things

import random
import string
import logging
import json
import httplib2
import requests
import pickle 
app = Flask(__name__)


# Connect to database and create database session
# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


# Display all things
@app.route('/')
def showMain():
    withVids, withoutVids = pickle.load(open('submissions.p', "rb"))
    return render_template('submissions.html', subwVideos= withVids, subWithoutVideos=withoutVids)
 
if __name__ == '__main__':
    app.debug = True
    app.run()