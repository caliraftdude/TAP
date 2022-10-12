"""
Class Player

The player class represents the client or "player" of the game.

XXX  It seems as if more should be in here, but that wont be certian 
until more of the code is reviewed.

"""
from .actor import Actor


class Player(Actor):
    def __init__(self):
        Actor.__init__(self, "you", True)
    
    def __repr__(self)->str:
        return "<Class 'Player'>"

    def __str__(self) -> str:
        return f"Player: XXX todo"

    def add_verb(self, name, f):
        self.verbs[name] = (lambda self: lambda *args: f(self, *args))(self)