"""
Audio manipulation.
"""

import logging
from pydub import AudioSegment
from helpers.logger import LOGGER
from helpers.queues import INBOUND_QUEUE, UPDATED_WAVE_QUEUE


def modify_wav(file_path):
    """
    Increse the volume of the wav file and save it.
    """

    try:
        file_upload = open(file_path, 'rb')
        wav_file = AudioSegment.from_file(file_upload)

        louder_wav_file = wav_file + 10
        louder_wav_file.export(file_path, "wav")

        LOGGER.info(f'File {file_path} has been modified.')
        file_upload.close()
        UPDATED_WAVE_QUEUE.put(file_path)
    except Exception as ex:
        LOGGER.exception(ex)
        raise ex


def wav_check():
    """
    Check for new wav files from the Inbound queue and process them.
    """
    while True:
        modify_wav(INBOUND_QUEUE.get())
