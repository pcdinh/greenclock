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
