# py-microsoft-cognitive-services
Thin wrapper for the Microsoft Cognitive Services

A continuation of: https://github.com/tristantao/py-bing-search


Intro
=====
Extremely thin python wrapper for Microsoft Cognitive Services API. Please note that this module does not use the older Microsoft Azure DataMarket WebSearch API (deprecated Dec 15 2016). This module requires that you sign up for Microsoft Cognitive Services and acquire application key for the corresponding services.

The modules uses OAuth, so you'll need to get your key here (free for up to 1K/Mon):
* [Subscribe for Free](https://www.microsoft.com/cognitive-services/en-us/sign-up)


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
>>> search_service = PyMsCognitiveWebSearch(('Your-Api-Key-Here', search_term)
>>> first_fifty_result= search_service.search(limit=50, format='json') #1-50
>>> second_fifty_result= search_service.search(limit=50, format='json') #51-100

>>> print (second_fifty_result[0].snippet)
    u'Python Software Foundation Home Page. The mission of the Python Software Foundation is to promote, protect, and advance the Python programming language, and to ...'
```
