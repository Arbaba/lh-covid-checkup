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
    ytPlaylist = "http://www.youtube.com/watch_videos?video_ids="
    ytIDS = [parser.videoID(sub[2], embed=False)  for sub in data['withVideos'] if 'youtube' in sub[2]]
    playlists =[]
    for i in range(0, int(len(ytIDS) / 50) + 1):
        playlists.append(ytPlaylist + ','.join(ytIDS[i * 50: min(len(ytIDS), (i+ 1) * 50)]))
    return render_template('submissions.html', subwVideos= data['withVideos'], subWithoutVideos=data['withoutVideos'], timestamp=data['time'], nProjects=nProjects, playlists=playlists)
 
if __name__ == '__main__':
    app.debug = True
    app.run()