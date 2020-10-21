"""
Queues and queue accessories.
"""

from queue import Queue


class Queing():
    """
    Stuff to manage queues. Jeez!
    """

    class Inbound(Queue):
        """
        Inbound queue stuff.
        """

        def __init__(self):
            super().__init__()

    class UpdatedWave(Queue):
        """
        Updated wave file queue.
        """

        def __init__(self):
            super().__init__()


INBOUND_QUEUE = Queing.Inbound()
UPDATED_WAVE_QUEUE = Queing.UpdatedWave()
