"""
Thread management.
"""

import threading
import ctypes
from helpers.logger import LOGGER


def get_id(thread):
    """
    Get ID of running thread.
    """

    for id, active_thread in threading._active.items():
        if active_thread is thread:
            return id


def raise_exception(thread):
    """
    Raise exception on current thread to terminate it.
    """

    thread_id = get_id(thread)
    LOGGER.debug(f'Thread ID: {thread_id}')

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)

    if res == 0:
        LOGGER.warning('Active thread does not exist.')
    elif res > 1:
        LOGGER.exception(
            'UH OH! Something happened :( Thread did not terminate.')
    else:
        LOGGER.info(f'Thread "{thread.name}" Terminated.')
