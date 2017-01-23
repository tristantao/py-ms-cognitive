import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch

##
##
## Image Search
##
##

class PyMsCognitiveImageException(Exception):
    pass

class PyMsCognitiveImageSearch(PyMsCognitiveSearch):

    SEARCH_IMAGE_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'

    def __init__(self, api_key, query, safe=False, custom_params=''):
        query_url = self.SEARCH_IMAGE_BASE + custom_params
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

        packaged_results = [ImageResult(single_result_json) for single_result_json in json_results["value"]]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results

class ImageResult(object):
    '''
    The class represents a SINGLE Image result.
    Each result will come with the following:

    the variable json will contain the full json object of the result.

    conten_url: duration of the Image
    name: name of the image / page title
    image_id: image id
    image_insights_token: image insights token
    web_search_url: the bing search url for the image
    host_page_url: the bing url to the host page
    content_size: size of the image
    thumbnail_url: url of the thumbnail

    Not included: lots of info, poke in json to see.
    '''

    def __init__(self, result):
        self.json = result
        self.content_url = result.get('contentUrl')
        self.name = result.get('name')
        self.image_id = result.get('ImageId')
        self.image_insights_token = result.get('imageInsightsToken')
        self.web_search_url = result.get('webSearchUrl')
        self.host_page_url = result.get('hostPageUrl')
        self.content_size = result.get('contentSize')
        self.thumbnail_url= result.get('thumbnailUrl')

