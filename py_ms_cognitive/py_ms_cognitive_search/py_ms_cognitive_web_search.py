import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker

##
##
## Web Search
##
##


class PyMsCognitiveWebSearch(PyMsCognitiveSearch):

    SEARCH_WEB_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/search'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False):
        query_url = self.SEARCH_WEB_BASE
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, custom_params, silent_fail=silent_fail)

    def _search(self, limit, format):
        '''
        Returns a list of result objects, with the url for the next page MsCognitive search url.
        '''
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {
          'q' : self.query,
          'count' : limit, #currently 50 is max per search.
          'offset': self.current_offset,
        }
        payload.update(self.CUSTOM_PARAMS)

        headers = { 'Ocp-Apim-Subscription-Key' : self.api_key }
        if not self.silent_fail:
            QueryChecker.check_web_params(payload, headers)
        response = requests.get(self.QUERY_URL, params=payload, headers=headers)
        json_results = self.get_json_results(response)
        packaged_results = [WebResult(single_result_json) for single_result_json in json_results.get("webPages", {}).get("value", [])]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results

class WebResult(object):
    '''
    The class represents a SINGLE search result.
    Each result will come with the following:

    the variable json will contain the full json object of the result.

    title: title of the result (alternately name)
    url: the url of the result. Seems to be a Bing redirect
    displayUrl: the url used to display
    snippet: description for the result (alternately description)
    id: MsCognitive id for the page
    '''

    def __init__(self, result):
        self.json = result
        self.url = result.get('url')
        self.display_url = result.get('displayUrl')
        self.name = result.get('name')
        self.snippet = result.get('snippet')
        self.id = result.get('id')

        #maintain compatibility
        self.title = result.get('name')
        self.description = result.get('snippet')

        self.deep_links = result.get('deepLinks')
