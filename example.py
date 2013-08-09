
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
    scheduler.schedule('task_1', func_1, greenclock.every(seconds=4))
    scheduler.schedule('task_2', func_2, greenclock.every(seconds=1))
    scheduler.run_forever(start_at=None)
