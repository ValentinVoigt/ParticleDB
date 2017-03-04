import requests
import json

OCTOPART_PARTS_SEARCH_URL = "http://octopart.com/api/v3/parts/search"
OCTOPART_PARTS_MATCH_URL = "http://octopart.com/api/v3/parts/match"

class Octopart:

    apikey = None

    def __init__(self, settings):
        self.apikey = settings['octopart_key']
        self.session = requests.Session()

    def search(self, search_text):
        r = self.session.get(OCTOPART_PARTS_SEARCH_URL, params={
            'apikey': self.apikey,
            'q': search_text,
        })
        r.raise_for_status()
        return r.json()

    def match(self, mpn):
        r = self.session.get(OCTOPART_PARTS_MATCH_URL, params={
            'apikey': self.apikey,
            'include[]': [
                'short_description',
                'datasheets',
                'descriptions',
                'imagesets',
                'specs',
            ],
            'queries': json.dumps([{
                'mpn': mpn,
            }]),
        })
        r.raise_for_status()
        return r.json()
