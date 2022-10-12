"""
Class Pet

A pet is an actor with free will (Animal) that you can also command to do things (Robot)
"""
from .robot import Robot
from .animal import Animal
from .constants import MessageType


class Pet(Robot, Animal):
    def __init__(self, name):
        super(Pet, self).__init__(name)
        self.leader = None
        self.verbs["heel"] = self.act_follow
        self.verbs["follow"] = self.act_follow
        self.verbs["stay"] = self.act_stay

    def __repr__(self)->str:
        return "<Class 'Pet'>"

    def __str__(self) -> str:
        return f"Todo"

    def act_follow(self, actor, words=None):
        self.leader = self.player
        self.output(
            "%s obediently begins following %s" % (self.name, self.leader.name),
            MessageType.FEEDBACK,
        )
        return True

    def act_stay(self, actor, words=None):
        if self.leader:
            self.output(
                "%s obediently stops following %s" % (self.name, self.leader.name),
                MessageType.FEEDBACK,
            )
        self.leader = None
        return True

    def act_autonomously(self, observer_loc):
        if self.leader:
            self.set_location(self.leader.location)
        else:
            self.random_move(observer_loc)