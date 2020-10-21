"""
Client main service.
"""

import atexit
from threading import Thread
from helpers.api_requests import PredictionAPI
from helpers.discovery import BROADCAST
import helpers.local_ops as LocalOps
from helpers.logger import LOGGER
from helpers.microphone import Audio
from helpers.queues import OUTBOUND_QUEUE

MIC_AUDIO = Audio()

LocalOps.create_temp_dir()
atexit.register(LocalOps.delete_temp_dir)

BROADCAST.start_discovery()
PREDICTION_API = PredictionAPI()


def outbound_queue_check():
    """
    Set some vars, check the queue and send shit.
    """

    try:
        while True:
            if MIC_AUDIO.mic_enabled and not BROADCAST.is_running:
                PREDICTION_API.__init__()
                next_file = OUTBOUND_QUEUE.get()
                PREDICTION_API.post_recording(next_file)
    except Exception as ex:
        LOGGER.exception(ex)
        raise ex


try:
    QUEUE_THREAD = Thread(target=outbound_queue_check, daemon=True, name='queue_svc')
    QUEUE_THREAD.start()
    MIC_AUDIO.record_audio()
except Exception as ex:
    LOGGER.exception(ex)
    raise ex
