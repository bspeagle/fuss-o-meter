"""
Network hub/client discovery.
"""

import json
import os
from socket import *
import sys
from helpers.logger import LOGGER


class Broadcast:
    """
    Broadcast for client discovery.
    """

    def __init__(self):
        self.is_running = bool

    def start_discovery(self):
        """
        Start discovery process.
        """

        LOGGER.info('Discovery started. Searching for hub.')

        self.is_running = True

        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.settimeout(5)

        server_address = ('255.255.255.255', 9434)
        message = 'pfg_ip_broadcast_cl'

        try:
            while True:
                try:
                    LOGGER.debug(f'Sending: {message}')
                    sent = sock.sendto(message.encode(), server_address)
                    LOGGER.debug(f'Sent: {sent}')

                    LOGGER.debug('Waiting to receive...')
                    data, server = sock.recvfrom(4096)

                    recv_data = json.loads(data)
                    LOGGER.debug(f'Received: {recv_data}')

                    if recv_data['message'] == 'pfg_ip_response_serv':
                        os.environ['HUB_PORT'] = recv_data['ackbar']
                        my_hostname = gethostname()
                        my_ip_address = gethostbyname(my_hostname)

                        if my_ip_address == server[0]:
                            os.environ['HUB_IP'] = 'localhost'
                        else:
                            os.environ['HUB_IP'] = server[0]

                        LOGGER.debug('Received confirmation.')
                        LOGGER.debug(
                            f"Server Addr: {os.getenv('HUB_IP')}:{os.getenv('HUB_PORT')}")
                        break
                    else:
                        LOGGER.warning('Verification failed.')
                except Exception as ex:
                    # [Errno 8]
                    if 'timed out' in str(ex):
                        LOGGER.warning(f'Waiting on hub to broadcast...')
                        continue
                    else:
                        LOGGER.exception(ex)
                        raise ex
        except Exception as ex:
            LOGGER.exception(ex)
            raise ex
        finally:
            sock.close()
            self.is_running = False


BROADCAST = Broadcast()
