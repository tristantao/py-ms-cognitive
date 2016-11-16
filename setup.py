from setuptools import setup, find_packages
import os
import platform

DESCRIPTION = "A simple lightweight python wrapper for the Microsoft Cognitive Services."
VERSION = '0.3.0'
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    'Topic :: Software Development :: Libraries :: Python Modules',
]

KEYWORDS = ['Microsoft', 'Cognitive Services', 'API', 'Search']

INSTALL_REQUIRES = [
    'requests',
]

setup(
    name='py-ms-cognitive',
    #packages = ['py-ms-cognitive'],
    packages = find_packages(),
    version=VERSION,
    author=u'Tristan Tao',
    author_email='tristan@teamleada.com',
    url='https://github.com/tristantao/py-ms-cognitive',
    license='MIT',
    keywords=KEYWORDS,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    test_suite='nose.collector',
    tests_require=['nose'],
)
