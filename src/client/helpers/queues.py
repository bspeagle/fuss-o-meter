"""
Queues and queue accessories.
"""

from queue import Queue


class Queing():
    """
    Stuff to manage queues. Jeez!
    """

    class Outbound(Queue):
        """
        Outbound queue stuff.
        """

        def __init__(self):
            super().__init__()

    class StreamData(Queue):
        """
        Stream data queue from mic.
        """

        def __init__(self):
            super().__init__()


OUTBOUND_QUEUE = Queing.Outbound()
