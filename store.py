from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from scripts import parser
# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things
from datetime import datetime

import random
import string
import logging
import json
import httplib2
import requests
import pickle
subs = parser.allSubmissions()
#TODO format
def storeSubmissions():
    subs = parser.allSubmissions()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("----- Fetch submissions -----")
    subsWithVideos, subsWithoutVideos  =  parser.findVideos(subs)
    data = {'time': timestamp,
            'withVideos': subsWithVideos,
            'withoutVideos': subsWithoutVideos}

    print(str(len(subs)) + " submissions fetched")
    pickle.dump(data, open("submissions.p", 'wb'))
    print("Submissions stored in submissions.p")
storeSubmissions()