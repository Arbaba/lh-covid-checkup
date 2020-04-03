import requests
from bs4 import BeautifulSoup
BASE_URL = 'https://lauzhack-against-covid-19.devpost.com/'
SUBMISSIONS_URL = BASE_URL + 'submissions'


def allSubmissions():
    soup = BeautifulSoup(requests.get(SUBMISSIONS_URL).text, 'html.parser')
    projectsDirtyURL = (soup.findAll('a', {'class': 'block-wrapper-link fade link-to-software'}))
    projectsURL = [p.get('href') for p in projectsDirtyURL]
    projectsTitles =soup.findAll('div', {'class': 'software-entry-name entry-body'})#.find_next('h5').text    
    titles = [p.find_next('h5').text.strip() for p in projectsTitles]
    return zip(titles, projectsURL)

def invalidSubmissions():
    subs = allSubmissions()
    r = []
    for title, url in subs:
        found = False
        for prop in ['Proposal', 'PROPOSAL', 'proposal']:
            if prop in title: 
                found = True
        if not found:
            r.append((title, url))

    return r