"""
Sound recording stuff.
"""

import os
import sys
import tempfile
import time
import sounddevice as sd
import soundfile as sf
from helpers.discovery import BROADCAST
from helpers.queues import OUTBOUND_QUEUE, Queing
from helpers.logger import LOGGER


class Audio():
    """
    Audio functions
    """

    class Tools():
        """
        Extra tools for stuff.
        """

        def int_or_str(self, text):
            """Helper function for argument parsing."""
            try:
                return int(text)
            except ValueError:
                return text

    def __init__(self):
        self.mic_enabled = True
        self.__stream_data_queue = Queing.StreamData()
        self.__rec_duration = int(os.getenv('REC_DURATION'))
        self.__temp_file_dir = os.getenv('TEMP_FILE_DIR')

    def record_audio(self):
        """
        Record audio.
        """

        # loop_count = 0

        def callback(stream_data, frame_count, time_info, status):
            """
            This is called (from a separate thread) for each audio block.
            """

            try:
                if status:
                    LOGGER.warning(f'{status} file={sys.stderr}')

                # LOGGER.debug(f"""
                # --- Input Stream ---
                # Frame Count: {frame_count}
                # Time Info: {time_info}
                # Status: {status}
                # Stream Data: {stream_data}
                # \n""")

                # if os.getenv('ENV') == 'dev':
                #     volume_norm = np.linalg.norm(stream_data) * 10
                #     LOGGER.info(f'Volume level: {volume_norm}')

                self.__stream_data_queue.put(stream_data.copy())
            except Exception as ex:
                LOGGER.exception(ex)
                raise ex

        try:
            while True:
                if self.mic_enabled and not BROADCAST.is_running:
                    temp_filename = tempfile.mktemp(prefix='temp_file-',
                                                    suffix='.wav', dir=self.__temp_file_dir)
                    with sf.SoundFile(temp_filename,
                                      mode='x', samplerate=44100, channels=2) as file:
                        with sd.InputStream(samplerate=44100, channels=2, callback=callback):
                            LOGGER.info(
                                f"""Recording...\nFile Path: {file.name}""")

                            start_time = time.time()

                            while True:
                                current_time = time.time()
                                elapsed_time = current_time - start_time

                                file.write(self.__stream_data_queue.get())

                                if elapsed_time > self.__rec_duration:
                                    OUTBOUND_QUEUE.put(file.name)
                                    # loop_count += 1
                                    break
        except Exception as ex:
            LOGGER.exception(ex)
            # raise ex
