GreenClock
==========

GreenClock is a time-based task scheduler using gevent

With GreenClock, you can: Schedule a task to run every X seconds, daily, weekly, monthly, 
or at certain times (such as application startup).

GreenClock launches a [green thread](http://en.wikipedia.org/wiki/Green_threads) per task.
Therefore every task will be executed in a concurrent manner, without blocking each other.

### Status

This module is currently under development.

### Features

    - A simple to use API for scheduling jobs.
    - Lightweight
    - Works with Python 2.7+
    - Support the following scheduling scenarios: 
        + run every X seconds
        + run every hour at specified minute and second
        + run at specified time (hour:minute:second) every day
        + more to come

### Installation

This library depends on gevent 1.0 RC2

```bash
    $ pip install cython -e git://github.com/surfly/gevent.git@1.0rc2#egg=gevent
```

To install GreenClock from [pip](https://pypi.python.org/pypi/pip):

```bash
    $ pip install greenclock
```


You can also install it into your Python application directory

```bash
    $ pip install --install-option="--prefix=/path/to/python/app" greenclock
```


To install GreenClock from source:
```bash
    $ git clone git@github.com:pcdinh/greenclock.git
    $ python setup.py install
```

### Usage

```

import greenclock
from datetime import datetime
import time

def func_1():
    print('Calling func_1() at ' + str(datetime.now()))
    time.sleep(2)
    print('Ended call to func_1() at ' + str(datetime.now()))

def func_2():
    print('Calling func_2() at ' + str(datetime.now()))
    time.sleep(2)
    print('Ended call to func_2() at ' + str(datetime.now()))

if __name__ == "__main__":
    scheduler = greenclock.Scheduler(logger_name='task_scheduler')
    scheduler.schedule('task_1', greenclock.every_second(4), func_1)
    scheduler.schedule('task_2', greenclock.every_second(1), func_2)
    # To start the scheduled tasks immediately, specify 'once' for `start_at`
    # Other values: 
    # * `next_minute`: Wait until the first seconds of the next minute to run
    # * `next_hour`: Wait until the first seconds of the next hour to run
    # * `tomorrow`: Wait until the first seconds of tomorrow to run
    scheduler.run_forever(start_at='once')

```
