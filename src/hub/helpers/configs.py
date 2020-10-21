"""
Various configs.
"""

import os
import secrets


class FlaskConfig(object):
    """
    Config base for Flask.
    """

    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(32)
    PORT = os.getenv('HUB_PORT')


class FlaskConfigDev(FlaskConfig):
    """
    Dev config for Flask.
    """

    ENV = 'development'
    DEBUG = True


class FlaskConfigCasual(FlaskConfig):
    """
    Casual config for Flask.
    """

    ENV = 'casual'
    DEBUG = False


class FlaskConfigProd(FlaskConfig):
    """
    Prod config for Flask.
    """

    ENV = 'production'
