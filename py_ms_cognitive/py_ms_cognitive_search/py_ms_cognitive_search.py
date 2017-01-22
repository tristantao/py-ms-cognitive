#!/usr/bin/env python
# encoding: utf-8

"""
Main class for doing actual searches.
"""

import time
import re


__author__ = 'tristantao (https://github.com/tristantao)'


class PyMsCognitiveException(Exception):
    pass


class PyMsCognitiveWebSearchException(Exception):
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
        self.most_recent_json = None

    def get_json_results(self, response):
        '''
        Parses the request result and returns the JSON object. Handles all errors.
        '''
        try:
            # return the proper JSON object, or error code if request didn't go through.
            self.most_recent_json = response.json()
            json_results = response.json()
            if response.status_code in [401, 403]: #401 is invalid key, 403 is out of monthly quota.
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
        return json_results

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


class QueryChecker():
    """
    Isolated human-error-checker class.
    All methods are static and do not modify state.
    if/else mess below forgoes optimization in favor of clarity.
    """
    @staticmethod
    def check_web_params(query_dict, header_dict):
        responseFilters = ('Computation', 'Images', 'News', 'RelatedSearches', 'SpellSuggestions', 'TimeZone', 'Videos', 'Webpages')

        if 'cc' in query_dict.keys():
            if query_dict['cc'] and not header_dict['Accept-Language']:
                raise AssertionError('Attempt to use country-code without specifying language.')
            if query_dict['mkt']:
                raise ReferenceError('cc and mkt cannot be specified simultaneously')
        if 'count' in query_dict.keys():
            if int(query_dict['count']) >= 51 or int(query_dict['count']) < 0:
                raise ValueError('Count specified out of range. 50 max objects returned.')
        if 'freshness' in query_dict.keys():
            if query_dict['freshness'] not in ('Day', 'Week', 'Month'):
                raise ValueError('Freshness must be == Day, Week, or Month. Assume Case-Sensitive.')
        if 'offset' in query_dict.keys():
            if int(query_dict['offset']) < 0:
                raise ValueError('Offset cannot be negative.')
        if 'responseFilter' in query_dict.keys():
            if query_dict['responseFilter'] not in responseFilters:
                raise ValueError('Improper response filter.')
        if 'safeSearch' in query_dict.keys():
            if query_dict['safeSearch'] not in ('Off', 'Moderate', 'Strict'):
                raise ValueError('safeSearch setting must be Off, Moderate, or Strict. Assume Case-Sensitive.')
            if 'X-Search-ClientIP' in query_dict.keys():
                raw_input('You have specified both an X-Search-ClientIP header and safesearch setting\nplease note: header takes precedence')
        if 'setLang' in query_dict.keys():
            if header_dict['Accept-Language']:
                raise AssertionError('Attempt to use both language header and query param.')
        if 'textDecorations' in query_dict.keys():
            if query_dict['textDecorations'].lower() not in ('true', 'false'):
                raise TypeError('textDecorations is type bool')
        if 'textFormat' in query_dict.keys():
            if query_dict['textFormat'] not in ('Raw', 'HTML'):
                raise ValueError('textFormat must be == Raw or HTML. Assume Case-Sensitive.')
        return True
