"""
Start up tasks.
"""

import os
from dotenv import load_dotenv
from helpers.ports import TCPPorts


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


def set_hub_port():
    """
    If HUB_PORT var doesn't exist, set it!
    """

    from helpers.logger import LOGGER

    if not os.getenv('HUB_PORT'):
        os.environ['HUB_PORT'] = str(TCPPorts().get_free_tcp_port())
        LOGGER.info(f"HUB_PORT: {os.getenv('HUB_PORT')}")
    else:
        LOGGER.info(f"HUB_PORT already set: {os.getenv('HUB_PORT')}")
