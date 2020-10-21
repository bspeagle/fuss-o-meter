"""
Hub service.
"""

import atexit
import os
import threading
import helpers.audio as Audio
import helpers.local_ops as LocalOps
import helpers.discovery as Discovery
import helpers.flask_api as Flask
from helpers.logger import LOGGER
import helpers.threads as Threads
from helpers.baby_detection.make_prediction import Predictomatica as Predictor

os.environ['HOME_DIR'] = os.getcwd()


try:
    PREDICTOR = Predictor()

    LocalOps.create_temp_dir()
    atexit.register(LocalOps.delete_temp_dir)

    DISC_SVC_THREAD = threading.Thread(
        target=Discovery.start_discovery, daemon=True, name='disc_svc')
    atexit.register(Threads.raise_exception, DISC_SVC_THREAD)
    DISC_SVC_THREAD.start()

    PREDICTOR_THREAD = threading.Thread(
        target=PREDICTOR.predict, daemon=True, name='predictor_svc')
    atexit.register(Threads.raise_exception, PREDICTOR_THREAD)
    PREDICTOR_THREAD.start()

    AUDIO_THREAD = threading.Thread(target=Audio.wav_check, daemon=True, name='audio_svc')
    atexit.register(Threads.raise_exception, AUDIO_THREAD)
    AUDIO_THREAD.start()

    Flask.start_api()

except Exception as ex:
    LOGGER.exception(ex)
    raise ex
