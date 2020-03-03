# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

from greenclock.version import __version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -r pypi')
    sys.exit()

VERSION = __version__[:__version__.index('.')]


def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.md')).read()


setup(
    name='greenclock',
    packages=['greenclock'],
    version=VERSION,
    description='A library that provides time-based task scheduling using green threads via gevent.',
    license='MIT',
    long_description=long_description(),
    install_requires=[
        'gevent>=1.5a3',
    ],
    author='Pham Cong Dinh',
    author_email='pcdinh@gmail.com',
    url='https://github.com/pcdinh/greenclock',
    download_url='https://github.com/pcdinh/greenclock/tarball/' + VERSION,
    keywords=[
        'cron', 'scheduling', 'schedule', 'periodic', 'jobs', 'clockwork', 'gevent'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
