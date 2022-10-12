"""
Class Game
# The Game: container for player, locations, robots, animals etc.

XXX
This is going to be the main engine for the game, organzing all of he objects and 
resources and presenting them to the application.
"""
from .schema.base import Base
from .schema.connection import Connection
from .schema.location import Location
from .schema.player import Player
from .schema.animal import Animal
from .schema.robot import Robot
from .schema.constants import MessageType, Direction



class Game(Base):
    def __init__(self, name="bwx-adventure"):
        Base.__init__(self, name)
        # self.objects = {}
        self.fresh_location = False
        self.player = None
        self.locations = {}
        self.robots = {}
        self.animals = {}

    # def set_name(self, name):
    #     self.name = name

    # add a bidirectional connection between points A and B
    def add_connection(self, connection):
        connection.game = self
        if isinstance(connection.way_ab, (list, tuple)):
            for way in connection.way_ab:
                connection.point_a.add_exit(connection, way)
        else:
            connection.point_a.add_exit(connection, connection.way_ab)

        # this is messy, need a better way to do this
        reverse_connection = Connection(
            connection.name,
            connection.point_b,
            connection.point_a,
            connection.way_ba,
            connection.way_ab,
        )
        reverse_connection.game = self
        if isinstance(connection.way_ba, (list, tuple)):
            for way in connection.way_ba:
                connection.point_b.add_exit(reverse_connection, way)
        else:
            connection.point_b.add_exit(reverse_connection, connection.way_ba)
        return connection

    def new_connection(self, *args):
        return self.add_connection(Connection(*args))

    # add another location to the game
    def add_location(self, location):
        location.game = self
        self.locations[location.name] = location
        return location

    def new_location(self, *args):
        return self.add_location(Location(*args))

    # add an actor to the game
    def add_actor(self, actor):
        actor.game = self

        if isinstance(actor, Player):
            self.player = actor

        if isinstance(actor, Animal):
            self.animals[actor.name] = actor

        if isinstance(actor, Robot):
            self.robots[actor.name] = actor

        return actor

    def new_player(self, location):
        self.player = Player()
        self.add_actor(self.player)
        self.player.set_location(location)
        return self.player

    def if_flag(self, flag, s_true, s_false, location=None):
        return lambda loc: (s_false, s_true)[flag in (location or loc).vars]

    def if_var(self, v, value, s_true, s_false, location=None):
        return lambda loc: (s_false, s_true)[
            v in (location or loc).vars and (location or loc).vars[v] == value
        ]

    # overload this for HTTP output
    def output(self, text, message_type=0):
        self.print_output(text, message_type)

    # checks to see if the inventory in the items list is in the user's inventory
    def inventory_contains(self, items):
        if set(items).issubset(set(self.player.inventory.values())):
            return True
        return False

    def entering_location(self, location):
        if self.player.location == location and self.fresh_location:
            return True
        return False

    def remove_superfluous_input(self, text):
        superfluous = self.articles + ["to"]
        rest = []
        for word in text.split():
            if word not in superfluous:
                rest.append(word)
        return " ".join(rest)

    def run(self, update_func=False):

        # reset this every loop so we don't trigger things more than once
        self.fresh_location = False

        actor = self.player
        while True:
            # if the actor moved, describe the room
            if actor.check_if_moved():
                self.output(
                    "        --=( %s %s in the %s )=--        "
                    % (actor.name.capitalize(), actor.isare, actor.location.name),
                    MessageType.TITLE,
                )

                # cache this as we need to know it for the query to entering_location()
                self.fresh_location = actor.location.first_time

                where = actor.location.describe(actor)
                if where:
                    self.output("")
                    self.output(where)
                    self.output("")

            # See if the animals want to do anything
            for animal in list(self.animals.items()):
                animal[1].act_autonomously(actor.location)

            # has the developer supplied an update function?
            if update_func:
                update_func()  # call the update function

            # check if we're currently running a script
            user_input = actor.get_next_script_line()
            if user_input == None:
                # get input from the user
                try:
                    self.output("")  # add a blank line
                    user_input = input("> ")
                except EOFError:
                    break
                if user_input == "q" or user_input == "quit":
                    break

            clean_user_input = self.remove_superfluous_input(user_input)

            # see if the command is for a robot
            if ":" in clean_user_input:
                robot_name, command = clean_user_input.split(":")
                try:
                    actor = self.robots[robot_name]
                except KeyError:
                    self.output("I don't know anybot named %s" % robot_name, MessageType.FEEDBACK)
                    continue
            else:
                actor = self.player
                command = clean_user_input

            # give the input to the actor in case it's recording a script
            if not actor.set_next_script_line(command):
                continue

            words = command.split()
            if not words:
                continue

            # first check phrases
            things = (
                list(actor.inventory.values())
                + list(actor.location.contents.values())
                + list(actor.location.actors)
                + [actor.location]
                + [actor]
            )
            done = False
            for thing in things:
                f = thing.get_phrase(command, things)
                if f:
                    f(self)
                    done = True
            if done:
                continue

            # Following the Infocom convention commands are decomposed into
            # VERB(verb), OBJECT(noun), INDIRECT_OBJECT(indirect).
            # For example: "hit zombie with hammer" = HIT(verb) ZOMBIE(noun) WITH HAMMER(indirect).

            target_name = ""
            if words[0].lower() == "tell" and len(words) > 2:
                target_name = words[1]
                words = words[2:]

            verb = words[0]
            words = words[1:]

            noun = None
            if words:
                noun = words[0]
                words = words[1:]

            indirect = None
            if len(words) > 1 and words[0].lower() == "with":
                indirect = words[0]
                words = words[2:]

            # if we have an explicit target of the verb, do that.
            # e.g. "tell cat eat foo" -> cat.eat( cat, 'food', [] )
            if target_name:
                done = False
                for a in actor.location.actors:
                    if a.name != target_name:
                        continue
                    f = a.get_verb(verb)
                    if f:
                        if f(a, noun, words):
                            done = True
                            break
                if done:
                    continue
                self.output("Huh? %s %s?" % (target_name, verb), MessageType.FEEDBACK)
                continue

            # if we have an indirect object, try it's handle first
            # e.g. "hit cat with hammer" -> hammer.hit( actor, 'cat', [] )
            if indirect:
                # try inventory and room contents
                done = False
                things = list(actor.inventory.values()) + list(
                    actor.location.contents.values()
                )
                for thing in things:
                    if indirect == thing.name:
                        f = thing.get_verb(verb)
                        if f:
                            if f(actor, noun, words):
                                done = True
                                break
                if done:
                    continue
                for a in actor.location.actors:
                    if indirect == a.name:
                        f = a.get_verb(verb)
                        if f:
                            if f(a, noun, words):
                                done = True
                                break
                if done:
                    continue

            # if we have a noun, try it's handler next
            if noun:
                done = False
                for thing in things:
                    if noun == thing.name:
                        f = thing.get_verb(verb)
                        if f:
                            if f(thing, actor, None, words):
                                done = True
                                break
                if done:
                    continue
                for a in actor.location.actors:
                    if noun == a.name:
                        f = a.get_verb(verb)
                        if f:
                            if f(a, None, words):
                                done = True
                                break
                if done:
                    continue

            # location specific verb
            f = actor.location.get_verb(verb)
            if f:
                if f(actor.location, actor, noun, words):
                    continue

            # handle directional moves of the actor
            if not noun:
                if verb in Direction.directions:
                    actor.act_go1(actor, verb, None)
                    continue

            # general actor verb
            f = actor.get_verb(verb)
            if f:
                if f(actor, noun, words):
                    continue

            # not understood
            self.output("Huh?", MessageType.FEEDBACK)