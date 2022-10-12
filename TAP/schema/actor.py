"""
Class Actor
An actor in the game
XXX
Actor is a base class for objects that can be interacted with and can take actions (?)


"""
from .constants import MessageType, Direction
from .base import Base



class Actor(Base):
    def __init__(self, name, player=False):
        Base.__init__(self, name)
        self.location = None
        self.inventory = {}
        self.cap_name = name.capitalize()
        self.player = player
        if player:
            self.isare = "are"
        else:
            self.isare = "is"
        # associate each of the known actions with functions
        self.verbs["take"] = self.act_multi(self.act_take1)
        self.verbs["get"] = self.act_multi(self.act_take1)
        self.verbs["drop"] = self.act_multi(self.act_drop1)
        self.verbs["inventory"] = self.act_inventory
        self.verbs["i"] = self.act_inventory
        self.verbs["look"] = self.act_look
        self.verbs["l"] = self.act_look
        self.verbs["go"] = self.act_go1
        self.verbs["verbs"] = self.act_list_verbs
        self.verbs["commands"] = self.act_list_verbs
        self.verbs["help"] = self.act_list_verbs

    def __repr__(self)->str:
        return "<Class 'Actor'>"

    def __str__(self) -> str:
        return f"Todo"

    # describe ourselves
    def describe(self, observer):
        return self.name

    # establish where we are "now"
    def set_location(self, loc):
        if not self.player and self.location:
            self.location.actors.remove(self)
        self.location = loc
        self.moved = True
        if not self.player:
            self.location.actors.add(self)

    # move a thing from the current location to our inventory
    def act_take1(self, actor, noun):
        if not noun:
            return False
        t = self.location.contents.pop(noun, None)
        if t:
            self.inventory[noun] = t
            self.output("You take the %s." % t.name)
            return True
        else:
            self.output("%s can't take the %s." % (self.cap_name, noun))
            return False

    # move a thing from our inventory to the current location
    def act_drop1(self, actor, noun):
        if not noun:
            return False
        t = self.inventory.pop(noun, None)
        if t:
            self.location.contents[noun] = t
            return True
        else:
            self.output(
                "%s %s not carrying %s."
                % (self.cap_name, self.isare, Base.add_article(noun)),
                MessageType.FEEDBACK,
            )
            return False

    def act_look(self, actor, noun, words):
        print(self.location.describe(actor, True))
        return True

    # list the things we're carrying
    def act_inventory(self, actor, noun, words):
        msg = "%s %s carrying " % (self.cap_name, self.isare)
        if list(self.inventory.keys()):
            msg += self.proper_list_from_dict(self.inventory)
        else:
            msg += "nothing"
        msg += "."
        self.output(msg, MessageType.FEEDBACK)
        return True

    # check/clear moved status
    def check_if_moved(self):
        status = self.moved
        self.moved = False
        return status

    # try to go in a given direction
    def act_go1(self, actor, noun, words):
        if not noun in Direction.directions:
            self.output("Don't know how to go '%s'." % noun, MessageType.FEEDBACK)
            return False
        loc = self.location.go(Direction.directions[noun])
        if loc == None:
            self.output("Bonk! %s can't seem to go that way." % self.name, MessageType.FEEDBACK)
            return False
        else:
            # update where we are
            self.set_location(loc)
            return True

    def act_many(self, f, actor, noun, words):
        result = True
        if not f(actor, noun):
            result = False
        # treat 'verb noun1 and noun2..' as 'verb noun1' then 'verb noun2'
        # treat 'verb noun1, noun2...' as 'verb noun1' then 'verb noun2'
        if words:
            for noun in words:
                noun = noun.strip(",")
                if noun in self.articles:
                    continue
                if noun == "and":
                    continue
                if not f(actor, noun):
                    result = False
        return result

    def act_multi(self, f):
        return (lambda f: (lambda a, n, w: self.act_many(f, a, n, w)))(f)

    def act_list_verbs(self, actor, noun, words):
        self.output("Here are the commands I understand:")
        self.output((lambda x: x)(" ".join(sorted(self.verbs.keys()))), MessageType.FEEDBACK)
        return True

    # support for scriptable actors, override these to implement
    def get_next_script_line(self):
        return None

    def set_next_script_line(self, line):
        return True