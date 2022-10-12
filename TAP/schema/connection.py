"""
Class Connection

A connection is an object that is used to "connect" to locations or objects
togeher.  This also supports one way and two way traversal.

XXX The functions and methods that should implement this dont seem to be 
*part* of this class... which is odd.  Need to review other parts of the
code and refactor accoringly.

This was likely a "great idea" initially.. and then scope and visibility
exceeded the authors skill to implement correctly.
"""
from .base import Base


# A "connection" connects point A to point B. Connections are
# always described from the point of view of point A.
class Connection(Base):
    # name
    # point_a
    # point_b

    def __init__(self, name, pa, pb, way_ab, way_ba):
        Base.__init__(self, name)
        self.point_a = pa
        self.point_b = pb
        self.way_ab = way_ab
        self.way_ba = way_ba

    def __repr__(self)->str:
        return "<Class 'Connection'>"

    def __str__(self) -> str:
        return f"Point_a: {self.point_a}\nPoint_b: {self.point_b}\nWay_ab: {self.way_ab}\nWay_ba: {self.way_ba}"