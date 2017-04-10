import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker

##
##
## Query Suggestions
##
##

class PyMsCognitiveSuggestions(PyMsCognitiveSearch):

    COGNITIVE_SUGGESTIONS_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/suggestions'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False):
        query_url = self.COGNITIVE_SUGGESTIONS_BASE
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, custom_params, silent_fail=silent_fail)

    def _search(self, limit, format):
        '''
        Returns a list of results objects
        '''
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {
            'q' : self.query,
            'mkt': 'en-us', #default, but can be overwritten.
            'count' : limit,
            'offset' : self.current_offset
        }
        payload.update(self.CUSTOM_PARAMS)

        headers = { 'Ocp-Apim-Subscription-Key': self.api_key }
        if not self.silent_fail:
            QueryChecker.check_web_params(payload, headers)
        response = requests.get(self.QUERY_URL, params=payload, headers=headers)
        json_results = self.get_json_results(response)
        packaged_results = [SuggestResult(single_result_json) for single_result_json in json_results.get("suggestionGroups", [])[0].get("searchSuggestions", [])]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results

class SuggestResult(object):
    '''
    The class represents a SINGLE suggest result.
    Each result will come with the following:

    the variable json will contain the full json object of the result.

    url: The URL for the suggestion. Internal to Bing, it seems
    query: The original query submited
    display_text: The suggestion generated
    search_kind: The type of search performed for the suggestion

    '''
    def __init__(self, result):
        self.json = result
        self.url = result.get('url')
        self.query = result.get('query')
        self.display_text = result.get('displayText')
        self.searck_kind = result.get('searchKind')
