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
filtersList = ['Topic', 'Does your team contain an EPFL student or staff member?', 'Are you interested to follow up on your project with EPFL initiatives?',  'Do you plan to pursue this project as a semester project?' ]

# Display all things
@app.route('/')
def index():

    data = pickle.load(open('crondata.p', "rb"))
    ytPlaylist = "http://www.youtube.com/watch_videos?video_ids="
    withVideos = data['withVideosComplete'] + data['withVideosNotComplete']
    nProjects = len(withVideos) + len(data['withoutVideos'])

    ytIDS = [parser.videoID(sub[2], embed=False)  for sub in withVideos if 'youtube' in sub[2]]
    playlists =[]
    for i in range(0, int(len(ytIDS) / 50) + 1):
        playlists.append(ytPlaylist + ','.join(ytIDS[i * 50: min(len(ytIDS), (i+ 1) * 50)]))
    return render_template('submissions.html', subwVideos=data['withVideosComplete'],  subWithoutVideos= data['withoutVideos'],
                            timestamp=data['time'], nProjects=nProjects, playlists=playlists, filters = filtersList)

if __name__ == '__main__':
    app.debug = True
    app.run()