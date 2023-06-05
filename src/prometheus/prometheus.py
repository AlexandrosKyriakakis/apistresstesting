import time

from prometheus_client import Gauge
from prometheus_client import Histogram


# Create a metric to track time spent and requests made.
REQUEST_TIME = Histogram(
    'request_processing_seconds',
    'Time spent processing request',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)


# # Workers
def time_histogram(histogram: Histogram):
    """A decorator that measures the time of a function in microseconds and observes that time in a Prometheus
    Histogram."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_time = time.perf_counter() - start_time
            histogram.observe(elapsed_time)
            return result

        return wrapper

    return decorator


FINAL_DELAY = Gauge('final_delay_nanos', 'Final Delay in nanos', ['country', 'date'])
END = Gauge('end_time_nanos', 'End time in nanos', ['country', 'date'])


# Data Worker
DATA_REQUEST_TIME = Histogram(
    'data_time_per_request',
    'Time spent in request',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)
DATA_SAVE_TIME = Histogram(
    'data_time_insert_db',
    'Time inserting in db',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)

# Daily Worker
DAILY_REQUEST_TIME = Histogram(
    'daily_time_per_request',
    'Time spent in request',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)
DAILY_PARSE_TIME = Histogram(
    'daily_time_parse',
    'Time parsing data',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)
DAILY_FORWARD_TIME = Histogram(
    'daily_time_forward',
    'Time forwarding data',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)
DAILY_SAVE_TIME = Histogram(
    'daily_time_insert_db',
    'Time inserting in db',
    buckets=(0.000000001, 0.00000001, 0.0000001, 0.000001, 0.0001, 0.01, 1, 10),
)

# Weekly Worker

# Monthly Worker
