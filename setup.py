# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup

from greenclock import __version__

# See: http://docs.python.org/3.1/distutils/uploading.html
# .pypirc file should look like:
# [pypirc]
#   servers = pypi
#   [server-login]
#     username:my_username
#     password:my_password
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -r pypi')
    sys.exit()

def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.md')).read()

setup(
    name='greenclock',
    packages=['greenclock'],
    version=__version__[:__version__.index('-')],
    description='gevent-based task scheduling library.',
    # LICENSE issue: https://github.com/josegonzalez/beaver/commit/1878b8a09b5e308d182f59def64b451f8ce4232d
    license='LICENSE.txt',
    long_description=long_description(),
    install_requires=[
        'gevent',
    ],
    author='Pham Cong Dinh',
    author_email='pcdinh@gmail.com',
    url='https://github.com/pcdinh/greenclock',
    download_url='https://github.com/pcdinh/greenclock/tarball/0.1.0',
    keywords=[
        'cron', 'scheduling', 'schedule', 'periodic', 'jobs', 'clockwork', 'gevent'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
