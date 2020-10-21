"""
API stuff for passing recordings to hub for predictions.
"""

import json
import os
from time import sleep
import requests
from helpers.discovery import BROADCAST
import helpers.local_ops as LocalOps
from helpers.logger import LOGGER


class PredictionAPI:
    """
    API stuff for predictions
    """

    def __init__(self):
        self.__hub_ip = os.getenv('HUB_IP')
        self.__hub_port = os.getenv('HUB_PORT')
        self.__post_endpoint = os.getenv('POST_ENDPOINT')
        self.__api_url = f'http://{self.__hub_ip}:{self.__hub_port}'

    def post_recording(self, file_path):
        """
        Send recording to prediction hub. Return predictions.
        """

        post_url = f'{self.__api_url}{self.__post_endpoint}'

        possible_errnos = [
            'Errno 32',
            'Errno 61',
            'Errno 111',
            'Errno 104',
            'Errno 101'
        ]

        try:
            upload_file = open(file_path, 'rb')
            files = {'audio_file': upload_file}

            response = requests.post(post_url, files=files)
            LOGGER.info(f'Response: <Status Code: {response.status_code}> {response.text}')

            upload_file.close()
            LocalOps.delete_file(file_path)
        except Exception as ex:
            if any(x in str(ex) for x in possible_errnos):
                LOGGER.warning('Hub Disconnected.')
                BROADCAST.start_discovery()
            else:
                LOGGER.exception(ex.args)
                raise ex

    def test_method(self, method, data):
        """
        Test stuff
        """

        get_endpoint = '/gimme'

        count = 0

        while count < 10:
            if method == 'GET':
                url = f'{self.__api_url}{get_endpoint}'
                response = requests.get(url)
                LOGGER.info(f'GET Response: {response.content}')
            elif method == 'POST':
                url = f'{self.__api_url}{self.__post_endpoint}'
                response = requests.post(url, json=data)
                response = json.loads(response.content)[0]

                LOGGER.info(f'POST Response: {response}')
            count += 1
            sleep(.5)
