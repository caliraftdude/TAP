"""
Class Location
    # name: short name of this location
    # description: full description
    # contents: things that are in a location
    # exits: ways to get out of a location
    # first_time: is it the first time here?
    # actors: other actors in the location

"""
from .constants import MessageType
from .base import Base
from .object import Object


# A "location" is a place in the game.
class Location(Base):
    def __init__(self, name, description):
        Base.__init__(self, name)
        self.description = description
        self.contents = {}
        self.exits = {}
        self.first_time = True
        self.actors = set()
        self.requirements = {}

    def __repr__(self)->str:
        return "<Class 'Location'>"

    def __str__(self) -> str:
        return f"TODO"

    def add_object(self, obj):
        self.contents[obj.name] = obj
        return obj

    def new_object(self, name, desc, fixed=False):
        return self.add_object(Object(name, desc, fixed))

    def description_str(self, d):
        if isinstance(d, (list, tuple)):
            desc = ""
            for dd in d:
                desc += self.description_str(dd)
            return desc
        else:
            if isinstance(d, str):
                return self.style_text(d, MessageType.DESCRIPTION)
            else:
                return self.description_str(d(self))

    def describe(self, observer, force=False):
        desc = ""  # start with a blank string

        # add the description
        if self.first_time or force:
            desc += self.description_str(self.description)
            self.first_time = False

        if self.contents:
            # try to make a readable list of the things
            contents_description = self.proper_list_from_dict(self.contents)
            # is it just one thing?
            if len(self.contents) == 1:
                desc += self.style_text(
                    "\nThere is %s here." % contents_description, MessageType.CONTENTS
                )
            else:
                desc += self.style_text(
                    "\nThere are a few things here: %s." % contents_description,
                    MessageType.CONTENTS,
                )

        if self.actors:
            for a in self.actors:
                if a != observer:
                    desc += self.style_text(
                        "\n"
                        + self.add_article(a.describe(a)).capitalize()
                        + " "
                        + a.isare
                        + " here.",
                        MessageType.CONTENTS,
                    )

        return desc

    def add_exit(self, con, way):
        self.exits[way] = con

    def go(self, way):
        if way in self.exits:
            c = self.exits[way]

            # check if there are any requirements for this room
            if len(c.point_b.requirements) > 0:
                # check to see if the requirements are in the inventory
                if set(c.point_b.requirements).issubset(
                    set(self.game.player.inventory)
                ):
                    self.output(
                        "You use the %s, the %s unlocks"
                        % (
                            self.proper_list_from_dict(c.point_b.requirements),
                            c.point_b.name,
                        ),
                        MessageType.FEEDBACK,
                    )
                    return c.point_b

                self.output(
                    "It's locked! You will need %s."
                    % self.proper_list_from_dict(c.point_b.requirements),
                    MessageType.FEEDBACK,
                )
                return None
            else:
                return c.point_b
        else:
            return None

    def debug(self):
        for key in self.exits:
            print("exit: %s" % key)

    def make_requirement(self, thing):
        self.requirements[thing.name] = thing