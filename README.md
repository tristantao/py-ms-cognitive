# py-ms-cognitive
Thin wrapper for the Microsoft Cognitive Services

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

####For Web Results:

```py
>>> from py_ms_cognitive import PyMsCognitiveWebSearch
>>> search_term = "Python Software Foundation"
>>> search_service = PyMsCognitiveWebSearch('API_KEY', search_term)
>>> first_fifty_result= search_service.search(limit=50, format='json') #1-50
>>> second_fifty_result= search_service.search(limit=50, format='json') #51-100

>>> print (second_fifty_result[0].snippet)
    u'Python Software Foundation Home Page. The mission of the Python Software Foundation is to promote, protect, and advance the Python programming language, and to ...'
```
