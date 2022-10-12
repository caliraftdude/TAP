from __future__ import annotations
from enum import Enum, auto

class MessageType(Enum):
    """
    MessageType controls the type of messaeing that is communicated to the console.  This
    can be used to change color, text, etc..
    """
    FEEDBACK = auto()
    TITLE = auto()
    DESCRIPTION = auto()
    CONTENTS = auto()

"""
Class Directions

XXX
Static class for maintaining the directions and associations to directions
directions and direction_name doesn't make any sense... the dictionary has both data items
already and while its not the intended use, or optimal, to search in the 
opposite manner.. this dict is not that big and we can clean this up 
a bit:

"""

# These are code-visible canonical names for directions for adventure authors
NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4
UP = 5
DOWN = 6
RIGHT = 7
LEFT = 8
IN = 9
OUT = 10
FORWARD = 11
BACK = 12
NORTH_WEST = 13
NORTH_EAST = 14
SOUTH_WEST = 15
SOUTH_EAST = 16
NOT_DIRECTION = -1

class Direction:
    # Class variables
    # A "direction" is all the ways you can describe going some way
    directions: dict[str,int] = {
        "north":NORTH,
        "n":NORTH,
        "south":SOUTH,
        "s":SOUTH,
        "east":EAST,
        "e":EAST,
        "west":WEST,
        "w":WEST,
        "up":UP,
        "u":UP,
        "down":DOWN,
        "d":DOWN,
        "right":RIGHT,
        "left":LEFT,
        "in":IN,
        "out":OUT,
        "forward":FORWARD,
        "fd":FORWARD,
        "fwd":FORWARD,
        "f":FORWARD,
        "back":BACK,
        "bk":BACK,
        "b":BACK,
        "nw":NORTH_WEST,
        "ne":NORTH_EAST,
        "sw":SOUTH_WEST,
        "se":SOUTH_EAST,
    }

    @staticmethod
    def dir(val: str)->None|int:
        return Direction.directions.get(val)

    @staticmethod
    def dir_name(val):
        retval = None  # default
        for key, value in Direction.directions.items():
            if value == val:
                return key


"""
The Colors class is used by style_text to add color and interest to responses.  Currently, 
its not implemented and honestly this is likely not the way to do it anyhow.  Its left
here as a reference for now until its factored out.
"""
# class Colors:
#     """
#     Colors class:
#     reset all colors with colors.reset
#     two subclasses fg for foreground and bg for background.
#     use as colors.subclass.colorname.
#     i.e. colors.fg.red or colors.bg.green
#     also, the generic bold, disable, underline, reverse, strikethrough,
#     and invisible work with the main class
#     i.e. colors.bold
#     """

#     reset = "\033[0m"
#     bold = "\033[01m"
#     disable = "\033[02m"
#     underline = "\033[04m"
#     reverse = "\033[07m"
#     strikethrough = "\033[09m"
#     invisible = "\033[08m"

#     class FG:
#         black = "\033[30m"
#         red = "\033[31m"
#         green = "\033[32m"
#         orange = "\033[33m"
#         blue = "\033[34m"
#         purple = "\033[35m"
#         cyan = "\033[36m"
#         lightgrey = "\033[37m"
#         darkgrey = "\033[90m"
#         lightred = "\033[91m"
#         lightgreen = "\033[92m"
#         yellow = "\033[93m"
#         lightblue = "\033[94m"
#         pink = "\033[95m"
#         lightcyan = "\033[96m"

#     class BG:
#         black = "\033[40m"
#         red = "\033[41m"
#         green = "\033[42m"
#         orange = "\033[43m"
#         blue = "\033[44m"
#         purple = "\033[45m"
#         cyan = "\033[46m"
#         lightgrey = "\033[47m"
