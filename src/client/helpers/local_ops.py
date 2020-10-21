"""
Local file operations.
"""

import os
import shutil
import tempfile
from helpers.logger import LOGGER


def create_temp_dir():
    """
    Create temp dir for filez.
    """

    try:
        temp_dir = os.getenv('TEMP_FILE_DIR')

        if not isinstance(temp_dir, type(None)):
            if os.path.exists(temp_dir):
                LOGGER.warning('Temp Directory Already Exists.')
            else:
                temp_dir = tempfile.mkdtemp()
                os.environ['TEMP_FILE_DIR'] = temp_dir
        else:
            temp_dir = tempfile.mkdtemp()
            os.environ['TEMP_FILE_DIR'] = temp_dir

            LOGGER.debug(f'Temp Dir: {temp_dir}')
    except Exception as ex:
        LOGGER.exception(ex)
        raise ex


def delete_temp_dir():
    """
    Delete local temp directory.
    """

    try:
        temp_dir = os.getenv('TEMP_FILE_DIR')

        if not isinstance(temp_dir, type(None)):
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                LOGGER.info(f'Temp Directory Deleted: {temp_dir}')
            else:
                LOGGER.warning(
                    f'Temp Directory {temp_dir} does not exist.')
        else:
            LOGGER.warning(
                f'No Temp Directory exists.')
    except Exception as ex:
        LOGGER.exception(ex)
        raise ex


def delete_file(file_path):
    """
    Delete a file.
    """

    try:
        os.remove(file_path)
        LOGGER.debug(f'File Deleted: {file_path}')
    except Exception as ex:
        LOGGER.exception(ex)
        raise ex
