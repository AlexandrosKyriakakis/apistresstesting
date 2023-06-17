import functools
import time

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram


# Create a metric to track time spent and requests made.
REQUEST_TIME = Histogram(
    'request_processing_seconds',
    'Time spent processing request',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
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


def async_time_histogram(histogram: Histogram):
    """A decorator that measures the time of a function in microseconds and observes that time in a Prometheus
    Histogram."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed_time = time.perf_counter() - start_time
            histogram.observe(elapsed_time)
            return result

        return wrapper

    return decorator


FINAL_DELAY = Gauge('final_delay_nanos', 'Final Delay in nanos', ['country', 'date'])
END = Gauge('end_time_nanos', 'End time in nanos', ['country', 'date'])


# Data Worker
DATA_TOTAL_BYTES_RECEIVED = Counter(
    'data_total_bytes_received', 'Data Worker Total Bytes received'
)
DATA_TOTAL_REQUESTS_PROCESSED = Counter(
    'data_total_requests_processed', 'Data Worker Total requests processed'
)

DATA_REQUEST_TIME = Histogram(
    'data_time_per_request',
    'Time spent in request',
    buckets=(
        0.000000001,
        0.000001,
        0.00001,
        0.0001,
        0.001,
        0.01,
        0.1,
        1,
        10,
        15,
        20,
        30,
        50,
        100,
        10000,
    ),
)
DATA_SAVE_TIME = Histogram(
    'data_time_insert_db',
    'Time inserting in db',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)

# Daily Worker

DAILY_TOTAL_BYTES_RECEIVED = Counter(
    'daily_total_bytes_received', 'Daily Worker Total Bytes received'
)
DAILY_TOTAL_BYTES_AFTER_PROCESS = Counter(
    'daily_total_bytes_after_process', 'Daily Worker Total Bytes after process'
)
DAILY_TOTAL_REQUESTS_PROCESSED = Counter(
    'daily_total_requests_processed', 'Daily Worker Total requests processed'
)

DAILY_REQUEST_TIME = Histogram(
    'daily_time_per_request',
    'Time spent in request',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
DAILY_PARSE_TIME = Histogram(
    'daily_time_parse',
    'Time parsing data',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
DAILY_FORWARD_TIME = Histogram(
    'daily_time_forward',
    'Time forwarding data',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
DAILY_SAVE_TIME = Histogram(
    'daily_time_insert_db',
    'Time inserting in db',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)

# Weekly Worker

WEEKLY_TOTAL_BYTES_RECEIVED = Counter(
    'weekly_total_bytes_received', 'Weekly Worker Total Bytes received'
)
WEEKLY_TOTAL_BYTES_AFTER_PROCESS = Counter(
    'weekly_total_bytes_after_process', 'Weekly Worker Total Bytes after process'
)
WEEKLY_TOTAL_REQUESTS_PROCESSED = Counter(
    'weekly_total_requests_processed', 'Weekly Worker Total requests processed'
)


WEEKLY_PARSE_TIME = Histogram(
    'weekly_time_parse',
    'Time parsing data',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
WEEKLY_FORWARD_TIME = Histogram(
    'weekly_time_forward',
    'Time forwarding data',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
WEEKLY_SAVE_TIME = Histogram(
    'weekly_time_insert_db',
    'Time inserting in db',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)

# Monthly Worker
MONTHLY_TOTAL_BYTES_RECEIVED = Counter(
    'monthly_total_bytes_received', 'Monthly Worker Total Bytes received'
)
MONTHLY_TOTAL_BYTES_AFTER_PROCESS = Counter(
    'monthly_total_bytes_after_process', 'Monthly Worker Total Bytes after process'
)
MONTHLY_TOTAL_REQUESTS_PROCESSED = Counter(
    'monthly_total_requests_processed', 'Monthly Worker Total requests processed'
)


MONTHLY_PARSE_TIME = Histogram(
    'monthly_time_parse',
    'Time parsing data',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
MONTHLY_FORWARD_TIME = Histogram(
    'monthly_time_forward',
    'Time forwarding data',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
MONTHLY_SAVE_TIME = Histogram(
    'monthly_time_insert_db',
    'Time inserting in db',
    buckets=(0.000000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10),
)
