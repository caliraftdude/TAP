"""
Class Animal

"""
import random
from .actor import Actor
from .constants import MessageType, Direction
from .base import Base


# Animals are actors which may act autonomously each turn
class Animal(Actor):
    def __init__(self, name):
        super(Animal, self).__init__(name)
        self.name = name

    def __repr__(self)->str:
        return "<Class 'Animal'>"

    def __str__(self) -> str:
        return f"Todo"

    def act_autonomously(self, observer_loc):
        self.random_move(observer_loc)

    def random_move(self, observer_loc):
        if random.random() > 0.2:  # only move 1 in 5 times
            return
        exit = random.choice(list(self.location.exits.items()))
        if self.location == observer_loc:
            self.output(
                "%s leaves the %s via the %s."
                % (
                    Base.add_article(self.name).capitalize(),
                    observer_loc.name,
                    exit[1].name,
                ),
                MessageType.FEEDBACK,
            )
        self.act_go1(self, Direction.direction_name[exit[0]], None)
        if self.location == observer_loc:
            self.output(
                "%s enters the %s via the %s."
                % (
                    Base.add_article(self.name).capitalize(),
                    observer_loc.name,
                    exit[1].name,
                ),
                MessageType.FEEDBACK,
            )
