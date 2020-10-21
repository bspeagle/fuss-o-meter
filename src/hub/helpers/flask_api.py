"""
Flask api to receive audio for predictions and send results.
"""

import os
from flask import Flask, request
from helpers.logger import LOGGER
from helpers.queues import INBOUND_QUEUE

FLASK_APP = Flask(__name__)


def start_api():
    """
    Crank it up!
    """

    app_env = os.getenv('ENV').upper()
    config_object = ''

    if app_env == 'DEV':
        config_object = 'helpers.configs.FlaskConfigDev'
    elif app_env == 'CASUAL':
        config_object = 'helpers.configs.FlaskConfigCasual'
    elif app_env == 'PROD':
        config_object = 'helpers.configs.FlaskConfigProd'
    else:
        raise f'ENV {app_env} does not have a matching config. Try again.'

    FLASK_APP.config.from_object(config_object)
    LOGGER.debug(f"Flask Config: {FLASK_APP.config.items()}")

    FLASK_APP.run(host='0.0.0.0', port=FLASK_APP.config.get('PORT'))


@FLASK_APP.route('/')
def index():
    """
    API index?
    """

    return '--- SOMETHING CLEVER! ---'


@FLASK_APP.route('/gimme', methods=['GET', 'POST'])
def do_stuff():
    """
    eh?
    """

    if request.method == 'GET':
        response = 'BLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAHBLAH'
    elif request.method == 'POST':
        response = f'Your Data: {request.data}'

    return response


@FLASK_APP.route('/magik', methods=['POST'])
def predict():
    """
    Prediction route.
    """

    try:
        file_upload = request.files["audio_file"]

        temp_dir = os.getenv('TEMP_FILE_DIR')
        temp_file_path = os.path.join(temp_dir, file_upload.filename)

        file_upload.save(temp_file_path)

        INBOUND_QUEUE.put(temp_file_path)

        return 'Mutha-fuckin success bitches!'
    except Exception as ex:
        LOGGER.exception(ex)
