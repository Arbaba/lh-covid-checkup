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
    nPages = len(soup.find('ul', {'class': 'pagination'}).find_all(recursive=False)) - 1
    
    submissions = getPageSubmissions(soup)
    if nPages > 1:
        for n in range(2, nPages):
            pageSubs = getPageSubmissions(pageSoup(SUBMISSIONS_URL + '?page=' + str(n)))
            submissions.extend(pageSubs) 
    return submissions
def videoID(url, embed=True):
    #TODO: Refactor in a nicer way
    if "youtube" in url:
        if embed:
            return url[url.find('embed/')+len('embed/'):]
        else:
            return url[url.find('v=')+2:url.find('&')]
    elif "vimeo" in url:
        if embed:
            return url[url.find('video/')+len('video/'):]
        else:
            return url[url.find('video/')+len('video/'):]

def formatVideoURL(url):
    if "youtube" in url:
        id = videoID(url)
        if id == 'TffiywvBeFo':
            id = 'PpOHFp68_YE'
        return 'https://www.youtube.com/watch?v={}&feature=emb_title'.format(id)
    elif "vimeo" in url:
        return 'https://vimeo.com/{}'.format(videoID(url))


def findVideos(submissions):
    yt,others, notFound = [],[],[]
    for (name, url) in submissions:
        v = getProjectVideo(url)
        print(v)
        if v is None:
            notFound.append((name, url))
        else:
            if 'youtube' in v:
                yt.append((name, url, formatVideoURL(v)))
            else:
                others.append((name, url, formatVideoURL(v)))
                #found.append((name, url, formatVideoURL(v)))
    
    return yt + others, notFound

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