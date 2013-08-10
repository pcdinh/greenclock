import os
import sys
from distutils.core import setup

# See: http://docs.python.org/3.1/distutils/uploading.html
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -r pypi')
    sys.exit()

setup(
    name='greenclock',
    packages=['greenclock'],
    version='0.1.0',
    description='gevent-based task scheduling library.',
    license=open('LICENSE.txt').read(),
    long_description=open("README.md").read(),
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
        'License :: Public Domain',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries'
    ],
)
