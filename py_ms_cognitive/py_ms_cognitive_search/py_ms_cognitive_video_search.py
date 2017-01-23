import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch

##
##
## Video Search
##
##

class PyMsCognitiveVideoException(Exception):
    pass

class PyMsCognitiveVideoSearch(PyMsCognitiveSearch):

    SEARCH_VIDEO_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/videos/search'

    def __init__(self, api_key, query, safe=False, custom_params=''):
        query_url = self.SEARCH_VIDEO_BASE + custom_params
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, safe=safe)

    def _search(self, limit, format):
        '''
        Returns a list of result objects, with the url for the next page MsCognitive search url.
        '''
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {
          'q' : self.query,
          'count' : limit, #currently 50 is max per search.
          'offset': self.current_offset,
          #'mkt' : 'en-us', #optional
          #'safesearch' : 'Moderate', #optional
        }
        headers = { 'Ocp-Apim-Subscription-Key' : self.api_key }
        response = requests.get(self.QUERY_URL, params=payload, headers=headers)

        json_results = self.get_json_results(response)

        packaged_results = [VideoResult(single_result_json) for single_result_json in json_results["value"]]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results

class VideoResult(object):
    '''
    The class represents a SINGLE Video result.
    Each result will come with the following:

    the variable json will contain the full json object of the result.

    duration: duration of the Video
    host_page_display_url: url shown for the page where the video is
    host_page_url: the bing url to the host page
    name: name of the object
    web_search_url: the bing search url for the video
    video_id: unique id for the video
    description: description for the result

    Not included: lots of info, poke in json to see.
    '''

    def __init__(self, result):
        self.json = result
        self.duration = result.get('duration')
        self.host_page_display_url = result.get('hostPageDisplayUrl')
        self.name = result.get('name')
        self.host_page_url = result.get('hostPageUrl')
        self.web_search_url = result.get('webSearchUrl')
        self.video_id = result.get('videoId')
        self.description= result.get('description')
