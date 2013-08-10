# coding: utf-8

import logging
import time
from datetime import timedelta, datetime
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

def every(*args, **kwargs):
    '''
    Iterator-based timer
    
    @example 
    >> every(seconds=10)
    >> every(hours=1)
    @return an iterator of timedelta object
    '''
    delta = timedelta(*args, **kwargs)
    while 1:
        yield delta

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

    def schedule(self, name, func, timer, *args, **kwargs):
        '''
        ts = Scheduler('my_task')
        ts.schedule(every(seconds=10), handle_message, "Every 10 seconds")
        ts.schedule(every(seconds=30), fetch_url, url="http://yahoo.com", section="stock_ticker")
        ts.run_forever()
        '''
        self.tasks.append(Task(name, func, timer, *args, **kwargs))

    def run(self, task):
        '''
        Runs a task and re-schedule it
        '''
        gevent.spawn(task.action, *task.args, **task.kwargs)
        try:
            # total_seconds is available in Python 2.7
            gevent.spawn_later(task.timer.next().total_seconds(), self.run, task)
        except StopIteration:
            pass

    def run_tasks(self):
        '''
        Runs all assigned task in separate green threads. If the task should not be run, schedule it
        '''
        pool = Pool(len(self.tasks))
        for task in self.tasks:
            pool.spawn(self.run, task)
        return pool

    def run_forever(self, start_at='once'):
        """
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
            while True:
                gevent.sleep(seconds=1)
            task_pool.join(timeout=30)
        except KeyboardInterrupt:
            # https://github.com/surfly/gevent/issues/85
            task_pool.closed = True
            task_pool.kill()
            logging.getLogger(self.logger_name).info('Time scheduler quits')
