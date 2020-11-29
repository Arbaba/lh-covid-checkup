import requests
from bs4 import BeautifulSoup
from urllib.parse import quote as urlFormat

#BASE_URL = 'https://lauzhack-against-covid-19.devpost.com/'
BASE_URL = 'https://lauzhack-5-0.devpost.com/'

SUBMISSIONS_URL = BASE_URL + 'submissions'

def pageSoup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def getPageSubmissions(soup):
    projectsDirtyURL = (soup.findAll('a', {'class': 'block-wrapper-link fade link-to-software'}))
    projectsURL = [p.get('href') for p in projectsDirtyURL]
    projectsTitles =soup.findAll('div', {'class': 'software-entry-name entry-body'})#.find_next('h5').text    
    titles = [p.find_next('h5').text.strip() for p in projectsTitles]
    return list(zip(titles, projectsURL))

def allSubmissions(startPageUrl):
    
    soup = BeautifulSoup(requests.get(startPageUrl).text, 'html.parser')
    pagination = soup.find('ul', {'class': 'pagination'})
    nPages = 1

    if pagination is not None: 
        nPages = len(soup.find('ul', {'class': 'pagination'}).find_all(recursive=False)) - 1
    submissions = getPageSubmissions(soup)

    if nPages > 1:
        binder='?'
        if '?' in startPageUrl:
            binder='&'
        for n in range(2, nPages):
            pageSubs = getPageSubmissions(pageSoup(startPageUrl + binder +'page=' + str(n)))
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

def findFilters(soup):
    filters = {} #{filtername -> [{'value': v, 'searchParams': p}]
    data = soup.find('form', {'class': 'filter-submissions'})
    if data is not None:
        for x in data.find_all('input'):
            if x.has_attr('name') and 'filter' in x['name']:
                filtername = x['name'].replace('[','').replace(']','').replace('filter','')#.capitalize()
                if filtername not in filters.keys():
                    filters[filtername] = [] 
                filters[filtername].append({'value': x['value'], 'searchParams': 'search?utf8=✓&{}={}'.format(urlFormat(x['name']), urlFormat(x['value']))})
    return filters
def assignFilter(subsURLS, filters):
    assignments= {}
    for filtername, options in filters.items():
        for option in options:
            subs = allSubmissions(SUBMISSIONS_URL + '/'+ option['searchParams'])
            for sub in subs:
                url = sub[1]
                if url not in assignments:
                    assignments[url] = [] 
                assignments[url].append({'name': filtername, 'value': option['value']})
    return assignments
def addFilterResult(subslist, filtersAssignments, orderedFilterNames):
    print(orderedFilterNames)
    completed = []
    notCompleted =[]
    #too slow boi
    for sub in subslist:
        url = sub[1]
        values = []
        if filtersAssignments.get(url) is not None:

            for fname in orderedFilterNames:
                found = False
 
                for filter_ in filtersAssignments[url]:
                    if fname == filter_['name']:
                        values.append(filter_['value'].capitalize())
                        found = True
            
                if not found:
                    values.append('N/A')
            completed.append(sub +tuple(values))
            print(url + ' ' + str(filtersAssignments[url]))
        else:
            notCompleted.append(sub)

    return completed, notCompleted

def completeSubmission(soup, subs, filters):

    x = assignFilter(subs, filters)
    if x is not None:
        x = addFilterResult(subs,x,filters.keys())
        print(x)
        return x
    else:
        print(subs)
        return {'submissions': subs} 
        
    
"""
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

    return r"""