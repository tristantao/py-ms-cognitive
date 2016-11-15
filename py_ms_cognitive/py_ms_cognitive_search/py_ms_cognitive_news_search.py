import requests, requests.utils
from py_ms_cognitive_search import PyMsCognitiveSearch

##
##
## News Search
##
##

class PyMsCognitiveNewsException(Exception):
    pass

class PyMsCognitiveNewsSearch(PyMsCognitiveSearch):

    SEARCH_NEWS_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/news/search'

    def __init__(self, api_key, query, safe=False, custom_params=''):
        query_url = self.SEARCH_NEWS_BASE + custom_params
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, safe=safe)

    def _search(self, limit, format):
        '''
        Returns a list of result objects, with the url for the next page MsCognitive search url.
        '''
        payload = {
          'q' : self.query,
          'count' : '50', #currently 50 is max per search.
          'offset': self.current_offset,
          #'mkt' : 'en-us', #optional
          #'safesearch' : 'Moderate', #optional
        }
        headers = { 'Ocp-Apim-Subscription-Key' : self.api_key }
        response = requests.get(self.QUERY_URL, params=payload, headers=headers)
        json_results = self.get_json_results(response)

        packaged_results = [NewsResult(single_result_json) for single_result_json in json_results["value"]]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results

class NewsResult(object):
    '''
    The class represents a SINGLE news result.
    Each result will come with the following:

    the variable json will contain the full json object of the result.

    category: category of the news
    name: name of the article (title)
    url: the url used to display.
    image_url: url of the thumbnail
    date_published: the date the article was published
    description: description for the result

    Not included: about, provider, mentions
    '''

    def __init__(self, result):
        self.json = result
        self.category = result.get('category')
        #self.about = result['about']
        self.name = result.get('name')
        self.url = result.get('url')
        try:
            self.image_url = result['image']['thumbnail']['contentUrl']
        except KeyError as kE:
            self.image_url = None
        self.date_published = result.get('datePublished')
        self.description = result.get('description')
