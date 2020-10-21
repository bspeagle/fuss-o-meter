"""
Record myself for model
"""

import os
from queue import Queue
import sys
import tempfile
import time
import numpy as np
import sounddevice as sd
import soundfile as sf

STREAM_QUEUE = Queue()
RECORDING_DURATION = 5


def callback(stream_data, frame_count, time_info, status):
    """
    Callback.
    """

    STREAM_QUEUE.put(stream_data.copy())


while True:
    FILENAME = tempfile.mktemp(prefix='custom-',
                               suffix='.wav', dir=f'{os.getcwd()}/baby_detection_ml/data/007 - bspeagle')

    with sf.SoundFile(FILENAME, mode='x', samplerate=44100, channels=2) as file:
        with sd.InputStream(samplerate=44100, channels=2, callback=callback):
            print('#' * 100)
            print(""" Recording...""")
            print('#' * 100)

            START_TIME = time.time()

            while True:
                CURRENT_TIME = time.time()
                ELAPSED_TIME = CURRENT_TIME - START_TIME

                file.write(STREAM_QUEUE.get())

                if ELAPSED_TIME > RECORDING_DURATION:
                    break
