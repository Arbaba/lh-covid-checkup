
from scripts import scraper
from models.submission import SubmissionEncoder
import click
import json
import requests
import os
import re

@click.command()
@click.argument('hackathon_url')
def main(hackathon_url):
    """Scrapes all projects from the hackathon and store them in a json.

    Usage : store.py hackathon_url

    Parameter hackathon_url is the hackathon home page on devpost. For example https://lauzhack-5-0.devpost.com
    """
    if hackathon_url[-1] == '/':
        hackathon_url = hackathon_url[: -1]

    if not hackathon_url.endswith('.devpost.com'): 
        raise ValueError('Wrong hackathon_url format. The url should have format https://[hackathon name].devpost.com')
    hackathon_name = hackathon_url[hackathon_url.find('//') + 2 : hackathon_url.find('devpost.com') -1]

    submissions_dict = scraper.scrape(hackathon_url, hackathon_name)
    subsWithVideos, subsWithoutVideos = split_videos(submissions_dict['submissions'])
    submissions_dict['submissions'] = subsWithVideos + subsWithoutVideos

    if not os.path.exists('data'):
        os.mkdir('data')
    output_path  = 'data/{}.json'.format(hackathon_name)

    with open(output_path, 'w' ) as file:
        s = json.dumps(submissions_dict, indent=True, cls=SubmissionEncoder)
        print(s)
        file.write(s)
    print('Submissions stored in {}'.format(output_path))

def split_videos(submissions):
    """Splits submissions which submissions which have linked a video to a demo video from those without videos.

    Parameters
    ----------
    submissions : list
        List of submission objects.
    """
    yt,others, notFound = [],[],[]
    for submission in submissions:
        
        if submission.url_video is None:
            notFound.append(submission)
        else:
            if 'youtube' in submission.url_video:
                yt.append(submission)
            else:
                others.append(submission)
                #found.append((name, url, format_video_url(v)))
    
    return yt + others, notFound


if __name__ == '__main__':
    main()