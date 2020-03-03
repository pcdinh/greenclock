
from greenclock.utils import Scheduler, every_second, every_hour
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


def func_3():
    print('Calling func_3() at ' + str(datetime.now()))
    time.sleep(2)
    print('Ended call to func_3() at ' + str(datetime.now()))


if __name__ == "__main__":
    scheduler = Scheduler(logger_name='task_scheduler')
    scheduler.schedule('task_1', every_second(4), func_1)
    scheduler.schedule('task_2', every_second(1), func_2)
    # Run at 41:00 every hour every day
    scheduler.schedule('task_3', every_hour(minute=41, second=0), func_3)
    # Run task at 12:35:00 every day
    scheduler.schedule('task_2', every_hour(hour=12, minute=35, second=0), func_2)
    # Starts the scheduling engine without delay
    scheduler.run_forever(start_at='once')
