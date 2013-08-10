# coding: utf-8

import datetime
import unittest
import mock
from gevent.event import AsyncResult
from gevent import sleep, Timeout, with_timeout

import greenclock
from greenclock import every

def func_1():
    return 100

class SchedulerTests(unittest.TestCase):

    def setUp(self):
        self.scheduler = greenclock.Scheduler()

    def tearDown(self):
        self.scheduler.stop()

    def test_builtin_timer(self):
        assert every(seconds=2).next().total_seconds() == 2
        assert every(hours=1).next().total_seconds() == 3600

    def test_task_assignment(self):
        INTERVAL = 2
        self.scheduler.schedule('task_1', func_1, every(seconds=INTERVAL))
        assert self.scheduler.tasks[0].name == 'task_1'
        greenlet1, greenlet2 = self.scheduler.run(self.scheduler.tasks[0])
        event1 = AsyncResult()
        greenlet1.link(event1)
        self.assertEqual(event1.get(), 100)
        sleep(3)
        assert greenlet2.ready() == True
        assert greenlet2.successful() == True
        greenlet2.kill()
        greenlet1.kill()
        assert greenlet2.value[0].get() == 100, 'Actual %s' % str(greenlet2.value[0].get())

if __name__ == '__main__':
    unittest.main()
