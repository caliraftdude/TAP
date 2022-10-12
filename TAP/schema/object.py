"""
XXX
Object Class
This doesn't seem to be implemented anywhere that I can see so its hard to tell
what its intended purpose is or was.

    name: short name of this thing
    description: full description
    fixed: is it stuck or can it be taken

XXX -> seen in:
    Location
    
"""
from .base import Base

class Object(Base):
    def __init__(self, name, desc, fixed=False):
        Base.__init__(self, name)
        self.description = desc
        self.fixed = fixed

    def __repr__(self) -> str:
        return "<Class 'Object'>"

    def __str__(self) -> str:
        return f"Description: {self.description}\nFixed {self.fixed}"

    def describe(self, observer):
        return self.name