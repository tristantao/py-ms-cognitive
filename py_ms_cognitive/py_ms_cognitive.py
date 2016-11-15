import requests, requests.utils
import time, re
import pdb

class PyMsCognitiveException(Exception):
    pass

class PyMsCognitiveSearch(object):
    """
    Shell class for the individual searches
    """
    def __init__(self, api_key, query, query_url, safe=False):
        self.api_key = api_key
        self.safe = safe
        self.current_offset = 0
        self.query = query
        self.QUERY_URL = query_url

    def search(self, limit=50, format='json'):
        ''' Returns the result list, and also the uri for next page (returned_list, next_uri) '''
        return self._search(limit, format)

    def search_all(self, limit=50, format='json'):
        ''' Returns a single list containing up to 'limit' Result objects'''
        desired_limit = limit
        results = self._search(limit, format)
        limit = limit - len(results)
        while len(results) < desired_limit:
            more_results = self._search(limit, format)
            if not more_results:
                break
            results += more_results
            limit = limit - len(more_results)
            time.sleep(1)
        return results

##
##
## Web Search
##
##

class PyMsCognitiveWebSearchException(Exception):
    pass

class PyMsCognitiveWebSearch(PyMsCognitiveSearch):

    SEARCH_WEB_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/search'

    def __init__(self, api_key, query, safe=False, custom_params=''):
        query_url = self.SEARCH_WEB_BASE + custom_params
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
        try:
            # return the proper JSON object, or error code if request didn't go through.
            json_results = response.json()
            if response.status_code in [401, 403]:
                raise PyMsCognitiveWebSearchException("CODE {code}: {message}".format(code=response.status_code,message=json_results["message"]) )
            elif response.status_code in [429]:
                message = json_results['message']
                try:
                    # extract time out seconds from response
                    timeout = int(re.search('in (.+?) seconds', message).group(1)) + 1
                    print ("CODE 429, sleeping for {timeout} seconds").format(timeout=str(timeout))
                    time.sleep(timeout)
                except (AttributeError, ValueError) as e:
                    if not self.safe:
                        raise PyMsCognitiveWebSearchException("CODE 429. Failed to auto-sleep: {message}".format(code=response.status_code,message=json_results["message"]) )
                    else:
                        print ("CODE 429. Failed to auto-sleep: {message}. Trying again in 5 seconds.".format(code=response.status_code,message=json_results["message"]))
                        time.sleep(5)
        except ValueError as vE:
            if not self.safe:
                raise PyMsCognitiveWebSearchException("Request returned with code %s, error msg: %s" % (r.status_code, r.text))
            else:
                print ("[ERROR] Request returned with code %s, error msg: %s. \nContinuing in 5 seconds." % (r.status_code, r.text))
                time.sleep(5)
        packaged_results = [WebResult(single_result_json) for single_result_json in json_results["webPages"]["value"]]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results

class WebResult(object):
    '''
    The class represents a SINGLE search result.
    Each result will come with the following:

    #For the actual results#
    title: title of the result
    url: the url of the result. Seems to be a Bing redirect.
    displayUrl: the url used to display.
    description: description for the result
    id: MsCognitive id for the page

    '''

    def __init__(self, result):
        self.url = result['url']
        self.display_url = result['displayUrl']
        self.name = result['name']
        self.snippet = result['snippet']
        self.id = result['id']

        #maintain compatibility
        self.title = result['name']
        self.description = result['snippet']


