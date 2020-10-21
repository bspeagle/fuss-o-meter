"""
test.
"""

from time import sleep
from helpers.logger import LOGGER
from helpers.queues import INBOUND_QUEUE


def test_inbound_put():
    """
    bleh.
    """

    count = 0
    while count < 600:
        count += 1
        INBOUND_QUEUE.put(f'Another item - {count}')
        sleep(.5)


def test_inbound_get():
    """
    bleh.
    """

    count = 0
    while count < 600:
        count += 1
        next_item = INBOUND_QUEUE.get()
        LOGGER.info(f'Next Item: {next_item}')
