# py-ms-cognitive
Thin wrapper for the Microsoft Cognitive Services (originally called Project Oxford with an endpoint at projectoxford.ai). If you have additional support you want, please make an issue.

A continuation of __[PyBingSearch](https://github.com/tristantao/py-bing-search)__ which will no longer be updated as of Nov 14th 2016.

Intro
=====
Extremely thin python wrapper for Microsoft Cognitive Services API. Please note that this module does not use the older Microsoft Azure DataMarket WebSearch API (deprecated Dec 15 2016). This module requires that you sign up for Microsoft Cognitive Services and acquire application key(s) for the corresponding service(s).

The modules require different microsoft keys for different services, so you'll need to get yours here (free for up to 1K/Mon for search): __[Subscribe for Free](https://www.microsoft.com/cognitive-services/en-us/sign-up)__

Installation
=====
#####for python 2.7.* 

```sh
pip install py-ms-cognitive
```

#####for python 3.*

```sh
pip3 install py-ms-cognitive
```

*Requires the requests library.

Usage
=====

Remember to set the `API_KEY` as your own.

###Searches [Web / Image / News / Video]

####For Web Results:

```py
>>> from py_ms_cognitive import PyMsCognitiveWebSearch
>>> search_term = "Python Software Foundation"
>>> search_service = PyMsCognitiveWebSearch('API_KEY', search_term)
>>> first_fifty_result = search_service.search(limit=50, format='json') #1-50
>>> second_fifty_resul t= search_service.search(limit=50, format='json') #51-100

>>> print (second_fifty_result[0].snippet)
    u'Python Software Foundation Home Page. The mission of the Python Software Foundation is to promote, protect, and advance the Python programming language, and to ...'
>>> print (first_fifty_result[0].__dict__.keys()) #see what variables are available.
['name', 'display_url', 'url', 'title', 'snippet', 'json', 'id', 'description']
    
    # To get individual result json:
>>> print (second_fifty_result[0].json)
...
   
    # To get the whole response json from the MOST RECENT response
    # (which will hold 50 individual responses depending on limit set):
>>> print (search_service.most_recent_json)
...
```
__*limit*__ parameter controls how many results to return in this single query, up to __*50*__. if you need more than 50, call __*search_all()*__ below, and use the __*quota*__ parameter to specify how many results.

####For Image Results:

```py
>>> from py_ms_cognitive import PyMsCognitiveImageSearch
>>> search_term = "puppies"
>>> search_service = PyMsCognitiveImageSearch('API_KEY', search_term)
>>> first_fifty_result = search_service.search(limit=50, format='json') #1-50
>>> second_fifty_result = search_service.search(limit=50, format='json') #51-100

>>> print (second_fifty_result[0].name)
    u'So cute - Puppies Wallpaper (14749028) - Fanpop'
>>> print (first_fifty_result[0].__dict__.keys()) #see what variables are available.
['name', 'web_search_url', 'content_size', 'image_insights_token', 'content_url', 'image_id', 'json', 'host_page_url', 'thumbnail_url']
```

The package also support Video (__PyMsCognitiveVideoSearch__), and News (__PyMsCognitiveNewsSearch__). Simply replace the imports and they'll work the same.

## Searching for a specific number of results.

You secan also run __*search_all*__ to keep searching until it fills your required quota. Note that this will make an unpredictable number of api calls (hence drains your credits).

```py
>>> from py_ms_cognitive import PyMsCognitiveWebSearch
>>> search_term = "puppies"
>>> search_service = PyMsCognitiveWebSearch('API_KEY', search_term)
>>> result_list = search_service.search_all(quota=130) # will return result 1 - 130 
# (around 130 results, sometimes more)
>>> result_list = search_service.search_all(quota=130, format='json') #will return result 131 to 260 
# sometimes a bit different, but roughly the number. Read below for the details.
```
Sometimes microsoft returns 36 results when you query for 30 (just an inexact number). This means py-ms-cognitive will truncate some results. Here's an example:

```
result_list = search_service.search_all(quota=80) 
```

This will likely be forced to run twice, first time getting __*50*__ (the max) from Micorosoft, and perhaps second time returning __*33*__ for some reason. py-ms-cognitive will truncate and return 80. But it also received __*83*__ in combined results. That means the next time you run the command from the same instance:
result_list = search_service.search(limit=20),
It won't return result number __*80-100*__, but rather result number __*83 - 103*__. But you would have no way of knowing this.


__*search_all()*__ is available in all PyBing*Search classes.

## Custom parameters
Custom parameters can be added via the __*custom_params*__ parameter: 
```py
>>> from py_ms_cognitive import PyMsCognitiveWebSearch
>>> search_term = "xbox"
>>> search_service = PyMsCognitiveWebSearch('API_KEY', search_term, custom_params='&offset=10')
# You can have multiple custom params, i.e. custom_params='offset=10&mkt=en-us&safesearch=Strict'
>>> result_list = search_service.search(limit=50) #will return 10-60, since we asked for 50 with an offset of 10.
```
*Note that offset (among other query parameters) are used internally, and your custom param will overwrite them*. This means in the above example, no matter how many times you call __*search()*__, it'll always return result # __*10-60*__, since it'll honor the offset request in __*custom_params*__.

## silent_fail mode
you can enable *__silent_fail__* (off by default) by:

```py
>>> from py_ms_cognitive import PyMsCognitiveWebSearch
>>> search_term = "puppies"
>>> search_service = PyMsCognitiveWebSearch('API_KEY', search_term, silent_fail=True)
...
```

*__silent_fail__* mode will do the following:
 * Bad parameters will not be checked
 * Any error will only print out and sleep for a few seconds to retry.
 * It will (to its best ability) not raise any exceptions.

#### Additional support on the way. If you have additional support you want, please make an issue.
