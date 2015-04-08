import logging
import datetime


def log_timing(task_name, logger):
    def my_decorator(f):
          def wrapper(*args, **kwagrs):
              now = datetime.datetime.now()
              result = f(*args, **kwagrs)
              dt = datetime.datetime.now() - now
              logger.info("%s - %s" % (task_name, dt))
              return result
          return wrapper
    return my_decorator


class with_log_timing(object):
    def __init__(self, task_name, logger):
        self.task_name = task_name
        self.logger = logger

    def __enter__(self):
        self.now = datetime.datetime.now()

    def __exit__(self, type, value, traceback):
        dt = datetime.datetime.now() - self.now
        self.logger.info("%s - %s" % (self.task_name, dt))    

