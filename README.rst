GreenClock
==========

|Travs-CI status| |Coverage Status|

GreenClock is a time-based task scheduler using gevent

With GreenClock, you can: Schedule a task to run every X seconds, daily,
weekly, monthly, or at certain times (such as application startup).

GreenClock launches a `green
thread <http://en.wikipedia.org/wiki/Green_threads>`__ per task.
Therefore every task will be executed in a concurrent manner, without
blocking each other.

Status
------

This module is currently under development.

Features
--------

::

    - A simple to use API for scheduling jobs.
    - Lightweight (depending on gevent only)
    - Works with Python 2.7+
    - Support the following scheduling scenarios: 
        + run every X seconds
        + run every hour at specified minute and second
        + run at specified time (hour:minute:second) every day
        + more to come

Installation
------------

This library depends on gevent 1.5

.. code:: bash

        $ pip install cython -e git://github.com/surfly/gevent.git@1.0rc2#egg=gevent

To install GreenClock from `pip <https://pypi.python.org/pypi/pip>`__:

.. code:: bash

        $ pip install greenclock

You can also install it into your Python application directory

.. code:: bash

        $ pip install --install-option="--prefix=/path/to/python/app" greenclock

To install GreenClock from source:

.. code:: bash

        $ git clone git@github.com:pcdinh/greenclock.git
        $ python setup.py install

Usage
-----

::

    from greenclock.utils import Scheduler
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
        scheduler = Scheduler(logger_name='task_scheduler')
        scheduler.schedule('task_1', greenclock.every_second(4), func_1)
        scheduler.schedule('task_2', greenclock.every_second(1), func_2)
        # Run hourly task at 41:00 every day
        scheduler.schedule('task_3', greenclock.every_hour(minute=41, second=0), func_3)
        # Run daily task at 12:35:00
        scheduler.schedule('task_2', greenclock.every_hour(hour=12, minute=35, second=0), func_2)    
        # To start the scheduled tasks immediately, specify 'once' for `start_at`
        # Other values: 
        # * `next_minute`: Wait until the first seconds of the next minute to run
        # * `next_hour`: Wait until the first seconds of the next hour to run
        # * `tomorrow`: Wait until the first seconds of tomorrow to run
        scheduler.run_forever(start_at='once')

Basically to schedule a periodic task or job, you need to specify the
following parameters:

::

    + Task name: `task_1`
    + A timer that let the scheduler know how to run a periodic task

::

            # run the task for every 4 seconds
            from greenclock.utils import every_second, every_hour
            every_second(4) 
            # run the task every day at 01:10:00
            every_hour(hour=1, minute=10, second=0)

::

    + A function or callable object
    + Optional parameters to the above function or callable object

::

            scheduler.schedule('task_1', greenclock.every_second(1), func_1, param1, param2, named_param=2)

``Scheduler`` object can run a separate process which never exits if you
want it to

::

        scheduler.run_forever(start_at='once')

|Bitdeli Badge| |githalytics.com alpha|

.. |Travs-CI status| image:: https://travis-ci.org/pcdinh/greenclock.png
   :target: https://travis-ci.org/pcdinh/greenclock
.. |Coverage Status| image:: https://coveralls.io/repos/pcdinh/greenclock/badge.png
   :target: https://coveralls.io/r/pcdinh/greenclock
.. |Bitdeli Badge| image:: https://d2weczhvl823v0.cloudfront.net/pcdinh/greenclock/trend.png
   :target: https://bitdeli.com/free
.. |githalytics.com alpha| image:: https://cruel-carlota.pagodabox.com/a7b875db36121c410c906c620f242458
   :target: http://githalytics.com/pcdinh/greenclock