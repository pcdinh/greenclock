# coding: utf-8

import datetime
import unittest
import mock
from gevent.event import AsyncResult
from gevent import sleep, Timeout, with_timeout

import greenclock
from greenclock import every_second, every_hour

class MockDate1(datetime.datetime):
    @classmethod
    def now(cls):
        return cls(2013, 8, 11, 0, 0, 0)

class MockDatetime(object):

    def __init__(self, new_datetime):
        self.old_datetime = datetime.datetime
        self.new_datetime_cls = new_datetime

    def __enter__(self):
        datetime.datetime = self.new_datetime_cls
        return self

    def __exit__(self, type, value, traceback):
        datetime.datetime = self.old_datetime
        return self

def func_1():
    return 100

class SchedulerTests(unittest.TestCase):

    def setUp(self):
        self.scheduler = greenclock.Scheduler()

    def tearDown(self):
        self.scheduler.stop()

    def test_builtin_timer_second(self):
        assert every_second(2).next().total_seconds() == 2
        assert every_second(3600).next().total_seconds() == 3600

    def test_builtin_timer_hour1(self):
        # Unable to mock the datetime.datetime.now using @mock.patch('datetime.datetime.now')
        # See http://stackoverflow.com/questions/4481954/python-trying-to-mock-datetime-date-today-but-not-working
        # datetime.datetime.now.return_value = datetime.datetime(2013, 8, 11, 0, 0, 0)
        with MockDatetime(MockDate1):
            timer = every_hour(minute=10, second=0)
            # First time
            delay1 = timer.next().total_seconds()
            assert delay1 == 10 * 60, 'Actual %s' % str(delay1)
            assert timer.next().total_seconds() == 60 * 60

    def test_builtin_timer_hour2(self):
        with MockDatetime(MockDate1):
            timer = every_hour(hour=1, minute=10, second=0)
            # First time
            delay1 = timer.next().total_seconds()
            assert delay1 == 60 + 10 * 60, 'Actual %s' % str(delay1)
            assert timer.next().total_seconds() == 24 * 60 * 60

    def test_task_assignment(self):
        # See https://github.com/surfly/gevent/blob/master/greentest/test__event.py
        INTERVAL = 2
        self.scheduler.schedule('task_1', every_second(INTERVAL), func_1)
        assert self.scheduler.tasks[0].name == 'task_1'
        greenlet1, greenlet2 = self.scheduler.run(self.scheduler.tasks[0])
        event1 = AsyncResult()
        greenlet1.link(event1)
        self.assertEqual(event1.get(), 100)
        assert greenlet2.ready() == False
        assert greenlet2.successful() == False
        sleep(INTERVAL)
        assert greenlet2.ready() == True
        assert greenlet2.successful() == True
        greenlet2.kill()
        greenlet1.kill()
        assert greenlet2.value[0].get() == 100, 'Actual %s' % str(greenlet2.value[0].get())

if __name__ == '__main__':
    unittest.main()
