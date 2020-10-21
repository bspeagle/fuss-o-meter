"""
Network hub/client discovery.
"""

import json
import os
from socket import *
import sys
from helpers.logger import LOGGER


def start_discovery():
    """
    Start network discovery broadcast.
    """

    sock = socket(AF_INET, SOCK_DGRAM)
    magic_word = 'pfg_ip_response_serv'

    try:
        server_address = ('', 9434)
        sock.bind(server_address)

        LOGGER.info('Start broadcasting and listening for clients...')

        while True:
            data, address = sock.recvfrom(4096)
            data = str(data.decode('UTF-8'))
            LOGGER.debug(
                f'Received {str(len(data))} bytes from {str(address)}')
            LOGGER.debug(f'Data: {data}')

            if data == 'pfg_ip_broadcast_cl':
                LOGGER.debug('Responding...')

                response = {
                    "message": magic_word,
                    "ackbar": os.getenv('HUB_PORT')
                }

                sent = sock.sendto(json.dumps(response).encode(), address)
                LOGGER.debug(f'Sent: {sent}')
                LOGGER.debug('Sent confirmation back')

        LOGGER.info('Discovery stopped.')
    except Exception as ex:
        LOGGER.exception(ex)
        raise ex
