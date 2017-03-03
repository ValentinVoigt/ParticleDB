import requests
import json

OCTOPART_PARTS_SEARCH_URL = "http://octopart.com/api/v3/parts/search"

class Octopart:

    apikey = None

    def __init__(self, settings):
        self.apikey = settings['octopart_key']
        self.session = requests.Session()

    def search(self, search_text):
        r = self.session.get(OCTOPART_PARTS_SEARCH_URL, params={
            'apikey': self.apikey,
            'include': [
                'short_description',
                'datasheets',
                'descriptions',
                'imagesets',
                'specs',
            ],
            'q': search_text,
        })
        r.raise_for_status()
        return r.json()

