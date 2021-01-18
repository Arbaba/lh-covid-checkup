import json
from json import JSONEncoder
class Submission():
    def __init__(self, title, url_submission, url_video, tags=[], filters=None):
        self.title = title
        self.url_submission = url_submission
        self.url_video = url_video
        self.filters = filters
        self.tags = tags 
    def __repr__(self):
        return str(vars(self))

class SubmissionEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, Submission):
            return object.__dict__
        return json.JSONEncoder.default(self, object)