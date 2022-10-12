"""
Game code

"""
import TAP
from TAP.schema.actor import Actor


def main() -> None:
    # Start by creating the game system
    game = TAP.Game("Sample Adventure")
    game = init(game)

    # Run the game
    game.run()

def init(game: TAP.Game)-> TAP.Game:
    # define and describe a couple of locations
    sidewalk = game.new_location(
        "Sidewalk",
        """There is a large glass door to the west.  The sign says 'Come In!'""",
    )

    vestibule = game.new_location(
        "Vestibule",
        """A small area at the bottom of a flight of stairs.  There is a glass door 
        to the east, and door to the west. To the north there is a dark muddy hole.""",
    )

    office = game.new_location(
        "Office",
        """A nicely organized office.  There is a door to the south.""",
    )

    tunnel = game.new_location(
        "Tunnel", """A dark and moist muddy hole that might lead somewhere..."""
    )

    # Define some connections
    game.new_connection("Glass Door", sidewalk, vestibule, [TAP.IN, TAP.WEST], [TAP.OUT, TAP.EAST])
    game.new_connection("Office Door", vestibule, office, [TAP.IN, TAP.WEST], [TAP.OUT, TAP.EAST])
    game.new_connection("Tunnel Opening", vestibule, tunnel, [TAP.DOWN, TAP.NORTH], [TAP.UP, TAP.SOUTH])

    # Now let's add a thing, a key, by providing a single word name and a longer
    # description.  We will create the key at the sidewalk.
    key = sidewalk.new_object("key", "a small tarnished key")
    ball = sidewalk.new_object("ball", "an unremarkable plastic ball")

    # And we can make the key required to open the office
    office.make_requirement(key)

    # Let's add a special phrase. We can attach this phrase to any object, location or actor,
    # and the phrase will trigger only if that object or actor is present or at the given location.
    key.add_phrase("rub key", game.say("You rub the key, but fail to shine it."))
    ball.add_phrase("rub ball", game.say("Look, this is pg-13 entertainment so.. keep it clean."))
    ball.add_verb("kick", game.say("The ball sails oddly, bounces on several random objects, and slowly returns to your feet."))
    ball.add_phrase("spit ball", game.say_on_noun("ball", "It seems to move on its own"))


    player = game.new_player(sidewalk)

    return game

if __name__ == '__main__':
    main()

#     flag_cases = [
#     ("hurt", True),
#     ("hungry", True),
#     ("Angry", True),
#     ("Tired", True),
#     ("10", True),
#     ("!@#@@", True),
# ]
#     from TAP.schema.base import Base
#     from TAP.schema.constants import MessageType

#     def test_flags():
#         base = Base("THISISATEST")
        
#         for a, b in flag_cases:
#             base.set_flag(a)
#             assert b==base.flag(a)

#         toggle = True
#         for a, b in flag_cases:
#             if toggle:
#                 base.unset_flag(a)
#                 assert b != base.flag(a)
#             else:
#                 assert b==base.flag(a)
#         toggle = not toggle

#     test_flags()
