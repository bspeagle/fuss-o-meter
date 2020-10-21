"""
Start up tasks.
"""

import os
from dotenv import load_dotenv


def load_env_vars():
    """
    Load system and .env vars
    """

    try:
        if not bool(os.getenv('DOTENV_LOADED')):
            load_dotenv()
            from helpers.logger import LOGGER
            LOGGER.info('Module dotenv Loaded!')
            os.environ['DOTENV_LOADED'] = str(True)
        else:
            from helpers.logger import LOGGER
            LOGGER.info('Module dotenv already loaded.')
    except Exception as ex:
        raise ex
