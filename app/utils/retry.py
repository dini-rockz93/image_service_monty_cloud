
import time
import random
import functools
def retry(exceptions, retries=5, base_delay=0.2, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == retries - 1:
                        raise
                    time.sleep(delay + random.uniform(0, delay))
                    delay *= backoff
        return wrapper
    return decorator
