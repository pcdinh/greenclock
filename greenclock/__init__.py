# coding: utf-8

import logging
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
from datetime import timedelta, datetime

def every(*args, **kwargs):
    delta = timedelta(*args, **kwargs)
    while 1:
        yield delta

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
        gevent.spawn(task.action, *task.args, **task.kwargs)
        try:
            # total_seconds is available in Python 2.7
            gevent.spawn_later(task.timer.next().total_seconds(), self.run, task)
        except StopIteration:
            pass

    def run_tasks(self):
        self.pool = Pool(len(self.tasks))
        for task in self.tasks:
            self.pool.spawn(self.run, task)

    def run_forever(self, start_at=None):
        """
        @param start_at: None -> start immediately
                         'minute' -> start at the first second of the next minutes
                         'hour' -> start 00:00 (min) next hour
                         'day' -> start at 0h next day
        """
        try:
            self.run_tasks()
            while True:
                gevent.sleep(seconds=1)
            self.pool.join(timeout=30)
        except KeyboardInterrupt:
            logging.getLogger(self.logger_name).info('Time scheduler quits')
