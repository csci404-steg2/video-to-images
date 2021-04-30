from dataclasses import dataclass

class HandshakeColors:
    """describes the constant colors of a frame handshake"""
    COLOR_DEAD_TIME = (0,0,0)

@dataclass
class HandshakeMeta:
    """describes the metadata found in a handshake
    members:
        dead_time - how much time to wait between data captures
        alive_time - how much time to actively capture data for
        offset_time - how much time to wait before attempting to capture data
        transmission_length - length (in bytes) of message
    """
    dead_time : int
    alive_time : int
    offset_time : int
    transmission_length : int