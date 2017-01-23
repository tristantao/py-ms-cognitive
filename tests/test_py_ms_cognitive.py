from unittest import TestCase
import time, ConfigParser
import os

from py_ms_cognitive import PyMsCognitiveWebSearch
from py_ms_cognitive import PyMsCognitiveImageSearch
from py_ms_cognitive import PyMsCognitiveVideoSearch
from py_ms_cognitive import PyMsCognitiveNewsSearch

def grab_search_secret():
    config = ConfigParser.ConfigParser()
    config.readfp(open('tests/secrets.cfg'))
    return config.get('secret', 'search_secret')

def setUpModule():
    global SECRET_KEY
    SECRET_KEY = grab_search_secret()
    print('Setting Up Test')

class TestPyMsCognitiveWebSearch(TestCase):

    def tearDown(self):
        '''To not overload API calls'''
        time.sleep(0.75)

    def test_can_search(self):
        web_bing = PyMsCognitiveWebSearch(SECRET_KEY, "Python Software Foundation")
        result_one = web_bing.search(limit=50)
        self.assertTrue(len(result_one) == 50)
        self.assertTrue("python" in result_one[0].name.lower())
        time.sleep

    def test_search_all(self):
        web_bing = PyMsCognitiveWebSearch(SECRET_KEY, "Python Software Foundation")
        result_one = web_bing.search_all(quota=60)
        self.assertTrue(len(result_one) == 60)
        self.assertTrue("python" in result_one[0].name.lower())

# Image Tests
class TestPyMsCognitiveImageSearch(TestCase):

    def tearDown(self):
        '''To not overload API calls'''
        time.sleep(0.75)

    def test_can_search(self):
        web_bing = PyMsCognitiveImageSearch(SECRET_KEY, "Python Software Foundation")
        result_one = web_bing.search(limit=50)
        self.assertTrue(len(result_one) == 50)
        self.assertTrue("python" in result_one[0].name.lower())

    def test_search_all(self):
        web_bing = PyMsCognitiveImageSearch(SECRET_KEY, "Python Software Foundation")
        result_one = web_bing.search_all(quota=60)
        self.assertTrue(len(result_one) == 60)
        self.assertTrue(len(result_one) == 60)
        self.assertTrue("python" in result_one[0].name.lower())

# Video Tests
class TestPyMsCognitiveVideoSearch(TestCase):

    def tearDown(self):
        '''To not overload API calls'''
        time.sleep(0.75)

    def test_can_search(self):
        web_bing = PyMsCognitiveVideoSearch(SECRET_KEY, "Python Software Foundation")
        result_one = web_bing.search(limit=50)
        self.assertTrue(len(result_one) == 50)
        self.assertTrue("python" in result_one[0].name.lower())

    def test_search_all(self):
        web_bing = PyMsCognitiveVideoSearch(SECRET_KEY, "Python Software Foundation")
        result_one = web_bing.search_all(quota=60)
        self.assertTrue(len(result_one) == 60)
        self.assertTrue("python" in result_one[0].name.lower())

# News Tests
class TestPyMsCognitiveNewsSearch(TestCase):

    def tearDown(self):
        '''To not overload API calls'''
        time.sleep(0.75)

    def test_can_search(self):
        web_bing = PyMsCognitiveNewsSearch(SECRET_KEY, "Python")
        result_one = web_bing.search(limit=50)
        self.assertTrue(len(result_one) > 0)
        self.assertTrue("python" in result_one[0].name.lower())

    def test_search_all(self):
        web_bing = PyMsCognitiveNewsSearch(SECRET_KEY, "Python")
        result_one = web_bing.search_all(quota=60)
        self.assertTrue(len(result_one) == 60)
        self.assertTrue("python" in result_one[0].name.lower())
