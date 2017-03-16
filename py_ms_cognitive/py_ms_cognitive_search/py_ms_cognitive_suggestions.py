import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker


##
##
## Query Suggestions
##
##

class PyMsCognitiveSuggestions(PyMsCognitiveSearch):

    SEARCH_WEB_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/search'

    def __init__(self, api_key, query, silent_fail=False, custom_params = ''):
        query_url = self.SEARCH_WEB_BASE
        self.custom_params_hash = dict(item.split("=") for item in custom_params.split("&")[1:])
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, silent_fail=silent_fail)
    
    def _search(self, limit, format):
        '''
        Returns a list of results objects
        '''
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {
            'q' : self.query,
             'count' : limit,
             'offset' : self.current_offset
        }
        payload.update(self.custom_params_hash)
        headers = { 'Ocp-Apim-Subscription-Key': self.api_key }
        if not self.silent_fail:
            QueryChecker.check_web_params(payload, headers)
        response = requests.get(self.QUERY_URL, params=payload, headers=headers)
        return response
        print("hey")