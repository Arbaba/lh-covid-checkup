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
import click

#TODO format
@click.command()
@click.option('--scrap', default=True,type=bool, required=False, help='Wheter to scrap devpost or to look locally before processing submissions')
def storeSubmissions(scrap):
    soup = parser.pageSoup(parser.SUBMISSIONS_URL)

    if scrap:
        subs = parser.allSubmissions(parser.SUBMISSIONS_URL)

        print("----- Fetch submissions -----")
        subsWithVideos, subsWithoutVideos  =  parser.findVideos(subs)
        filters = parser.findFilters(soup)
        print(str(len(subs)) + " submissions fetched")

    else:
        #TODO Fix this
        data = pickle.load(open('crondata.p', "rb"))
        filters = data['filters']
        
        subsWithVideos, subsWithoutVideos = data['withVideosComplete'], data['withoutVideos']
        subsWithoutVideos = data['withoutVideos']
        print(str(len(subsWithVideos + subsWithoutVideos)) + " submissions fetched")

    complete, notComplete = parser.completeSubmission(soup, subsWithVideos, filters)
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {'time': timestamp,
            'withVideosComplete': sortByStaff(complete),
            'withVideosNotComplete': notComplete,
            'withoutVideos': subsWithoutVideos,
            'filters': filters
            }
    pickle.dump(data, open("crondata.p", 'wb'))
    print("Submissions stored in crondata.p")

def sortByStaff(subslist):
    epfl = [sub for sub in subslist if sub[4] == 'Yes' ]
    notepfl = [sub for sub in subslist if sub[4] != 'Yes']
    return epfl + notepfl

if __name__ == '__main__':
    storeSubmissions()