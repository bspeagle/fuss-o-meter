"""
TCP port stuff.
"""

import socket


class TCPPorts:
    """
    TCP Port stuff.
    """

    def get_free_tcp_port(self):
        """
        Get a random open TCP port.
        """

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        addr, port = tcp.getsockname()

        tcp.close()

        return port

    def get_free_tcp_address(self):
        """
        Get a random open TCP address.
        """

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        host, port = tcp.getsockname()

        tcp.close()

        return 'tcp://{host}:{port}'.format(**locals())
