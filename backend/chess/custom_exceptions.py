class RoomError(Exception):
    """Base class for room-related errors."""

class RoomNotFoundError(RoomError):
    """Raised when a room is not found."""

class RoomFullError(RoomError):
    """Raised when a room is full."""

class InvalidInputError(RoomError):
    """Raised when input is invalid."""