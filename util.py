"""
FUnctions used all over.  Mostly time related.
Shit should I call this something time related instaed?
"""
from functools import wraps
from datetime import datetime, timedelta
import time

def default_start_end_times(start_date=None, end_date=None):
    """

    """
    pass

def get_intervals(start_date, end_date, **kwargs):
    """
    Given two dates, get list of intervals between them.
    Args:
        start_date: datetime, oldest date to being
        end_date: datetime, lats interval
        **kwargs: info about what sort of interval to put into effect, look up datetime.timedelta doc for more info
    Returns:
        list of datetimes
    """    
    invervals = []
    while start_date <= end_date:
        invervals.append(start_date)
        start_date = start_date + timedelta(**kwargs)
    return invervals

def time_function(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_count()
    return wrapper_funct