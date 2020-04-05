import requests
from bs4 import BeautifulSoup
BASE_URL = 'https://lauzhack-against-covid-19.devpost.com/'
SUBMISSIONS_URL = BASE_URL + 'submissions'

def pageSoup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def getPageSubmissions(soup):
    projectsDirtyURL = (soup.findAll('a', {'class': 'block-wrapper-link fade link-to-software'}))
    projectsURL = [p.get('href') for p in projectsDirtyURL]
    projectsTitles =soup.findAll('div', {'class': 'software-entry-name entry-body'})#.find_next('h5').text    
    titles = [p.find_next('h5').text.strip() for p in projectsTitles]
    return list(zip(titles, projectsURL))
def allSubmissions():
    soup = BeautifulSoup(requests.get(SUBMISSIONS_URL).text, 'html.parser')
    nPages = len(soup.find('ul', {'class': 'pagination'}).find_all(recursive=False)) - 2
    
    submissions = getPageSubmissions(soup)
    #hardcoded number of pages assumption
    for n in range(2, nPages):
        pageSubs = getPageSubmissions(pageSoup(SUBMISSIONS_URL + '?page=' + str(n)))
        submissions.extend(pageSubs) 
    return submissions
def formatVideoURL(url):
    print(url)

    if "youtube" in url:
        return 'https://www.youtube.com/watch?v={}&feature=emb_title'.format(url[url.find('embed/')+len('embed/'):])
    elif "vimeo" in url:
        return 'https://vimeo.com/{}'.format(url[url.find('video/')+len('video/'):])
def findVideos(submissions):
    found, notFound = [],[]
    for (name, url) in submissions:
        v = getProjectVideo(url)
        if v is None:
            notFound.append((name, url))
        else:
            found.append((name, url, formatVideoURL(v)))
    return found, notFound

def getProjectVideo(projectURL):
    soup = pageSoup(projectURL)
    iframe = soup.find('iframe',{'class':'video-embed'})#['src']
    if iframe is None:
        return None
    else:
        videoURL = iframe['src']
        takeUntil = max(0, videoURL.find('?'))
        return videoURL[:takeUntil]


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