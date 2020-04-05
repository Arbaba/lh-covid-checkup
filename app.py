from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from scripts import parser
from datetime import datetime

import random
import string
import logging
import json
import httplib2
import requests
import pickle 
app = Flask(__name__)

# Display all things
@app.route('/')
def index():
    data = pickle.load(open('submissions.p', "rb"))
    nProjects = len( data['withVideos']) + len(data['withoutVideos'])

    return render_template('submissions.html', subwVideos= data['withVideos'], subWithoutVideos=data['withoutVideos'], timestamp=data['time'], nProjects=nProjects)
 
if __name__ == '__main__':
    app.debug = True
    app.run()