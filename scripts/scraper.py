import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.submission import Submission  
from urllib.parse import quote as urlFormat


def scrape(hackathon_url, hackathon_name):
    """Scrapes all submissions from the hackathon and return them with some metatadata as a dict.
   
    Usage : store.py hackathon_url

    Parameters
    ----------
    hackathon_url : string
        Hackathon home page on devpost. For example : https://lauzhack-5-0.devpost.com
    
    hackathon_name: string
        hackathon name that will be stored in the returned dictionnary

    Returns
    -------
    dict
        Dictionnary with the hackathon name, list of submissions, filters and scraping timestamp.
    """

    submissions_url = hackathon_url + '/project-gallery'
    filters_url = hackathon_url + '/submissions'

    data = get_hackathon_data(submissions_url, filters_url)
    data['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data['hackathon_name'] = hackathon_name
    return data

def page_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_page_submissions(soup):
    """Returns the list of all submissions in the given page.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object of a page from the hackathon project gallery. 

    Returns
    -------
    list
        List of Submission objects.
    """
    projects_dirty_url = (soup.findAll('a', {'class': 'block-wrapper-link fade link-to-software'}))
    projects_url = [p.get('href') for p in projects_dirty_url]
    projects_title =soup.findAll('div', {'class': 'software-entry-name entry-body'})#.find_next('h5').text    
    titles = [p.find_next('h5').text.strip() for p in projects_title]
    submissions  = []
    for title, url_project, (url_video, tags) in list(zip(titles, projects_url, map(project_data, projects_url))):
        submissions.append(Submission(title, url_project, url_video, tags))
    return submissions


def get_all_submissions(project_gallery_url):
    """Returns the list of all submissions in the hackathon project gallery. 
    The pagination will be handled automatically.

    Parameters
    ----------
    project_gallery_url : string
        The url to the first page of the hackathon project gallery. To fetch submissions from the project gallery, the url must be similar to https://lauzhack-against-covid-19.devpost.com/project-gallery.
        Urls such as https://lauzhack-against-covid-19.devpost.com/submissions are deprecated and only work when used to fetch submissions with filters as explained below.
        To fetch filtered projects, the url is expected to be have a format similar to https://lauzhack-against-covid-19.devpost.com/submissions/search?utf8=%E2%9C%93&filter%5Btopic%5D%5B%5D=hospitals+and+medical+supplies.       
    Returns
    -------
    list
        List of Submission objects.
    """

    soup = page_soup(project_gallery_url)
    pagination = soup.find('ul', {'class': 'pagination'})
    nPages = 1
    #print("Extracting submissions. This operation can take a few minutes.")

    if pagination is not None: 
        nPages = len(soup.find('ul', {'class': 'pagination'}).find_all(recursive=False)) - 1
    submissions = get_page_submissions(soup)

    if nPages > 1:
        binder='?'
        if '?' in project_gallery_url:
            binder='&'
        for n in range(2, nPages):
            #print('{}/{} Pages extracted. Extracting page {}'.format(n -1,  nPages, n))
            soup = page_soup(project_gallery_url + binder +'page=' + str(n))
            pageSubs = get_page_submissions(soup)
            submissions.extend(pageSubs)

    #print('{}/{} Pages extracted.'.format(nPages, nPages))
    #print("Found {}".format(len(submissions)))
    return submissions


def video_id(url, embed=True):
    """Extracts the id contained in the video URL. Only youtube and vimeo URLs are supported.

    Parameters
    ----------
    url : string

    Returns
    -------
    string
        The video id.
    """

    if "youtube" in url:
        if embed:
            return url[url.find('embed/')+len('embed/'):]
        else:
            return url[url.find('v=')+2:url.find('&')]
    elif "vimeo" in url:
            return url[url.find('video/')+len('video/'):]
    else:
        raise Exception("Expected the video url to be from youtube or vimeo. Found {}".format(url))


def format_video_url(video_url):
    """Formats the video url found on devpost in order to redirect to the corresponding video on the video-sharing platform. 
        Supports youtube and vimeo videos. URLs from other platforms will not be formatted.

    Parameters
    ----------
    url : string
    """

    if "youtube" in video_url:
        id = video_id(video_url)
        if id == 'TffiywvBeFo':
            id = 'PpOHFp68_YE'
        return 'https://www.youtube.com/watch?v={}&feature=emb_title'.format(id)
    elif "vimeo" in video_url:
        return 'https://vimeo.com/{}'.format(video_id(video_url))
    else:
        return video_url

def get_tags(project_soup):
    return [li.text for li in  project_soup.findAll('span', {'class': 'cp-tag'})]


def get_video_url(project_soup):
    """Returns the video url in the specified project page.

    Parameters
    ----------
    project_url : string
        Project url in the format https://devpost.com/software/[project-name].

    Returns
    -------
    string
        The video url
    """

    iframe = project_soup.find('iframe',{'class':'video-embed'})#['src']
    if iframe is None:
        return None
    else:
        video_url = iframe['src']
        take_until = max(0, video_url.find('?'))
        return format_video_url(video_url[:take_until])

def project_data(project_url):
    """Return submission specific data"""

    project_soup = page_soup(project_url)
    return get_video_url(project_soup), get_tags(project_soup)


def find_filters(project_gallery_soup):
    """Map each filter to its list of possible values and corresponding search parameters."""

    filters = {} #{filtername -> [{'value': v, 'searchParams': p}]
    data = project_gallery_soup.find('form', {'class': 'filter-submissions'})
    if data is not None:
        for x in data.find_all('input'):
            if x.has_attr('name') and 'filter' in x['name']:
                filtername = x['name'].replace('[','').replace(']','').replace('filter','')#.capitalize()
                if filtername not in filters.keys():
                    filters[filtername] = [] 
                filters[filtername].append({'value': x['value'], 'searchParams': 'search?utf8=✓&{}={}'.format(urlFormat(x['name']), urlFormat(x['value']))})
    return filters
    
def assign_filters(filters, filters_url):
    """Map each submission URLs to its selected filters. As some submissions might not have
    selected any filter, the returned dictionnary might not contain all hackathon submissions.

    Parameters
    ----------
    filters_url : string
    filters : dict
    """
    assignments= {} #{submission_url -> [{'name': filtername, 'value': option['value']}}, ...]}
    for filtername, options in filters.items():
        for option in options:
            #print(FILTERS_URL + '/'+ option['searchParams'])
            subs = get_all_submissions(filters_url + '/'+ option['searchParams'])
            for sub in subs:
                if sub.url_submission not in assignments:
                    assignments[sub.url_submission] = [] 
                assignments[sub.url_submission].append({'name': filtername, 'value': option['value']})

    return assignments

def add_filter_results(submissions, filter_assignments, filters_names):
    """Returns a tuple of submissions updated with their selected filters and submissions for which not filter was selected.
    
    Parameters
    ----------
    submissions : list
    filter_assignments : dict
    filters_names : list
    """
    submissions_with_filters, submission_without_filter = [], []

    for sub in submissions:
        sub.filters = {}

        #Initialize filters
        for fname in filters_names:
            sub.filters[fname.capitalize()] = None
            
        #Update filters
        if filter_assignments.get(sub.url_submission) is not None:
            for fname in filters_names:
                found = False

                #Find the filter value
                for filter_ in filter_assignments[sub.url_submission]:
                    if fname == filter_['name']:
                        value = filter_['value'].capitalize()
                        found = True
            
                if not found:
                    value = None
                sub.filters[fname.capitalize()] = value
            submissions_with_filters.append(sub)
        else:
            submission_without_filter.append(sub)

    return submissions_with_filters, submission_without_filter

def get_hackathon_data(project_gallery_url, filters_url):
    """Fetches submissions with filters and returns them as a dict.

    Parameters
    ----------
    submissions_url : string
        The URL to the project gallery, such as https://lauzhack-against-covid-19.devpost.com/project-gallery.
    filters_url : string
        The base URL which supports filters queries, such as https://lauzhack-against-covid-19.devpost.com/submissions. 
    """
    print('Fetch submissions. This operation can take a few minutes...')
    subs = get_all_submissions(project_gallery_url)

    print(str(len(subs)) + ' submissions fetched')
    print('Fetch submissions filters...')

    soup = page_soup(project_gallery_url)
    filters = find_filters(soup)
    #dict filters_per_submission only contains submissions which had at least one filter selected.
    filters_per_submission = assign_filters(filters, filters_url)
    if filters_per_submission is not None:
        submissions_with_filters, submission_without_filter = add_filter_results(subs, filters_per_submission,filters.keys())

        return {
            'filters': [filter.capitalize() for filter in filters.keys()],
            'submissions': submissions_with_filters + submission_without_filter
        } 
    else:
        return {
            'filters': None,
            'submissions': subs
        }

