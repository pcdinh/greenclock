# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup

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
    version='0.1.1',
    description='gevent-based task scheduling library.',
    license='MIT',
    long_description=long_description(),
    data_files=[("", ["LICENSE.txt"])],
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
