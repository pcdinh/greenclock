# coding: utf-8
# license: MIT
"""A library to provide an interface to schedule and manage periodic tasks using `gevent`.
To use the library, you need to import the module first    
    import greenclock
    
Tasks are managed by `Scheduler` objects
    
    scheduler = greenclock.Scheduler(logger_name='task_scheduler')
    
You can register scheduled tasks with `Scheduler` object

    scheduler.schedule('task_1', greenclock.every_second(4), func_1)
    scheduler.schedule('task_2', greenclock.every_second(1), func_2)
    
Basically to schedule a periodic task or job, you need to specify the following parameters:

    + Task name: `task_1`
    + A timer that let the scheduler know how to run a periodic task
        
        # run the task for every 4 seconds
        greenclock.every_second(4) 
        # run the task every day at 01:10:00
        greenclock.every_hour(hour=1, minute=10, second=0)
        
    + A function or callable object
    + Optional parameters to the above function or callable object
    
        scheduler.schedule('task_2', greenclock.every_second(1), func_2, param1, param2, named_param=2)
    
`Scheduler` object can run a separate process which never exits if you want it to

    scheduler.run_forever(start_at='once')
"""

from . import version
__version__ = version.__version__

import types
import logging
import time
from datetime import timedelta, datetime
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

def every_second(seconds):
    '''
    Iterator-based timer

    @example 
    >> every(seconds=10)
    @return an iterator of timedelta object
    '''
    delta = timedelta(seconds=seconds)
    # Never return StopIteration
    while 1:
        yield delta

class every_hour(object):
    '''
    A class-based iterator that help install a timer for hourly scheduled task
    - Every hour in a day
    - Fixed hour in a day
    
    The name is chosen in all lower case to make it looks like a function because it will 
    be used as if it was a generator.
    '''
    def __init__(self, hour=None, minute=0, second=0):
        self.started = False
        self.hour = hour
        self.minute = minute
        self.second = second
    def __iter__(self):
        return self
    def next(self):
        '''
        Never return StopIteration
        '''
        if self.started is False:

            self.started = True
            now_ = datetime.now()
            if self.hour:
                # Fixed hour in a day
                # Next run will be the next day
                scheduled = now_.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=0)
                if scheduled == now_:
                    return timedelta(seconds=0)
                elif scheduled < now_:
                    # Scheduled time is passed
                    return scheduled.replace(day=now_.day + 1) - now_
            else:
                # Every hour in a day
                # Next run will be the next hour
                scheduled = now_.replace(minute=self.minute, second=self.second, microsecond=0)
                if scheduled == now_:
                    return timedelta(seconds=0)
                elif scheduled < now_:
                    # Scheduled time is passed
                    return scheduled.replace(hour=now_.hour + 1) - now_
            return scheduled - now_
        else:
            if self.hour:
                return timedelta(days=1)  # next day
            return timedelta(hours=1)  # next hour

def wait_until(time_label):
    '''
    Calculates the number of seconds that the process needs to sleep 
    '''
    if time_label == 'next_minute':
        gevent.sleep(60 - int(time.time()) % 60)
    elif time_label == 'next_hour':
        gevent.sleep(3600 - int(time.time()) % 3600)
    elif time_label == 'tomorrow':
        gevent.sleep(86400 - int(time.time()) % 86400)

class Task(object):
    '''
     A scheduled task
    '''
    def __init__(self, name, action, timer, *args, **kwargs):
        self.name = name
        self.action = action
        self.timer = timer
        self.args = args
        self.kwargs = kwargs

class Scheduler(object):
    '''
    Time-based scheduler
    '''
    def __init__(self, logger_name='greenlock.task'):
        self.logger_name = logger_name
        self.tasks = []
        self.active = {}  # action task name registry
        self.waiting = {}  # action task name registry
        self.running = True

    def schedule(self, name, timer, func, *args, **kwargs):
        '''
        ts = Scheduler('my_task')
        ts.schedule(every(seconds=10), handle_message, "Every 10 seconds")
        ts.schedule(every(seconds=30), fetch_url, url="http://yahoo.com", section="stock_ticker")
        ts.run_forever()
        '''
        self.tasks.append(Task(name, func, timer, *args, **kwargs))
        self.active[name] = []  # list of greenlets
        self.waiting[name] = []

    def unschedule(self, task_name):
        '''
        Removes a task from scheduled jobs but it will not kill running tasks
        '''
        for greenlet in self.waiting[task_name]:
            try:
                gevent.kill(greenlet)
            except BaseException:
                pass

    def stop_task(self, task_name):
        '''
        Stops a running or dead task
        '''
        for greenlet in self.active[task_name]:
            try:
                # Do not need to check if greenlet is dead, gevent does it already
                gevent.kill(greenlet)
                self.active[task_name] = []
            except BaseException:
                pass

    def _remove_dead_greenlet(self, task_name):
        '''
        Removes dead greenlet or done task from active list
        '''
        for greenlet in self.active[task_name]:
            try:
                # Allows active greenlet continue to run
                if greenlet.dead:
                    self.active[task_name].remove(greenlet)
            except BaseException:
                pass

    def run(self, task):
        '''
        Runs a task and re-schedule it
        '''
        self._remove_dead_greenlet(task.name)
        if isinstance(task.timer, types.GeneratorType):
            # Starts the task immediately
            greenlet_ = gevent.spawn(task.action, *task.args, **task.kwargs)
            self.active[task.name].append(greenlet_)
            try:
                # total_seconds is available in Python 2.7
                greenlet_later = gevent.spawn_later(task.timer.next().total_seconds(), self.run, task)
                self.waiting[task.name].append(greenlet_later)
                return greenlet_, greenlet_later
            except StopIteration:
                pass
            return greenlet_, None
        # Class based timer
        try:
            if task.timer.started is False:
                delay = task.timer.next().total_seconds()
                gevent.sleep(delay)
                greenlet_ = gevent.spawn(task.action, *task.args, **task.kwargs)
                self.active[task.name].append(greenlet_)
            else:
                greenlet_ = gevent.spawn(task.action, *task.args, **task.kwargs)
                self.active[task.name].append(greenlet_)
            greenlet_later = gevent.spawn_later(task.timer.next().total_seconds(), self.run, task)
            self.waiting[task.name].append(greenlet_later)
            return greenlet_, greenlet_later
        except StopIteration:
            pass
        return greenlet_, None

    def run_tasks(self):
        '''
        Runs all assigned task in separate green threads. If the task should not be run, schedule it
        '''
        pool = Pool(len(self.tasks))
        for task in self.tasks:
            # Launch a green thread to schedule the task
            # A task will be managed by 2 green thread: execution thread and scheduling thread
            pool.spawn(self.run, task)
        return pool

    def run_forever(self, start_at='once'):
        """
        Starts the scheduling engine
        
        @param start_at: 'once' -> start immediately
                         'next_minute' -> start at the first second of the next minutes
                         'next_hour' -> start 00:00 (min) next hour
                         'tomorrow' -> start at 0h tomorrow
        """
        if start_at not in ('once', 'next_minute', 'next_hour', 'tomorrow'):
            raise ValueError("start_at parameter must be one of these values: 'once', 'next_minute', 'next_hour', 'tomorrow'")
        if start_at != 'once':
            wait_until(start_at)
        try:
            task_pool = self.run_tasks()
            while self.running:
                gevent.sleep(seconds=1)
            task_pool.join(timeout=30)
            task_pool.kill()
        except KeyboardInterrupt:
            # https://github.com/surfly/gevent/issues/85
            task_pool.closed = True
            task_pool.kill()
            logging.getLogger(self.logger_name).info('Time scheduler quits')

    def stop(self):
        '''
        Stops the scheduling engine
        '''
        self.running = False
