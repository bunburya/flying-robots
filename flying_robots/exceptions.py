"""These are errors and exceptions that are used in multiple files
throughout the program."""

class GameError(Exception):
    """A base exception class for in-game errors, such as trying to move onto
    an invalid tile."""
    pass

class BadTileError(GameError):
    """Some moveable object has attempted to move onto a bad tile."""
    pass

class GameEvent(Exception):
    """A base exception class for certain events, such as the game ending or
    a level being completed, that may occur during the game."""
    pass

class GameOver(GameEvent):
    """Game is over, probably because player has died."""
    pass

class LevelComplete(GameEvent):
    """The level is complete."""
    pass
