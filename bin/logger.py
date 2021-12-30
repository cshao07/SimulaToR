import time
from functools import wraps


def logger(fn):
    """
    Recording options and run time.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(kwargs['command'])
        local_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print('Start SimCal %s at %s' % (kwargs['name'], local_time))
        fn(*args)
        local_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print('End SimCal %s at %s' % (kwargs['name'], local_time))

    return wrapper
