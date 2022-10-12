"""
Base is a place to put default inplementations of methods that everything
in the game should support (eg save/restore, how to respond to verbs etc)

XXX It doesn't seem to be doing, or refined for its documented purpose.. might
need to refactor accordingly
"""
from .constants import MessageType

class Base(object):
    def __init__(self, name)->None:
        self.game = None
        self.name = name
        self.verbs: dict = {}
        self.phrases: dict = {}
        self.vars: dict = {}
        self.articles = ["a", "an", "the"]  # XXX not sure - going to try here

    def __repr__(self)->str:
        return "<Class 'Base'>"

    def __str__(self) -> str:
        return f"Name: {self.name}\nVerbs: {self.verbs}\nPhrases: {self.phrases}\nVars: {self.vars}\nGame: {self.game}"

    def flag(self, f):
        if f in self.vars:
            return self.vars[f]
        else:
            return False

    def set_flag(self, f):
        self.vars[f] = True

    def unset_flag(self, f):
        if f in self.vars:
            del self.vars[f]

    def do_say(self, s):
        self.output(s, MessageType.FEEDBACK)
        return True

    def say(self, s):
        return (lambda s: lambda *args: self.do_say(s))(s)

    def do_say_on_noun(self, n, s, actor, noun, words):
        if noun != n:
            return False
        self.output(s, MessageType.FEEDBACK)
        return True

    def say_on_noun(self, n, s):
        return (
            lambda n, s: lambda actor, noun, words: self.do_say_on_noun(
                n, s, actor, noun, words
            )
        )(n, s)

    def say_on_self(self, s):
        return (
            lambda s: lambda actor, noun, words: self.do_say_on_noun(
                None, s, actor, noun, words
            )
        )(s)

    def add_verb(self, verb, f):
        self.verbs[" ".join(verb.split())] = f

    def get_verb(self, verb):
        c = " ".join(verb.split())
        if c in self.verbs:
            return self.verbs[c]
        else:
            return None

    def add_phrase(self, phrase, f, requirements=[]):
        self.phrases[" ".join(phrase.split())] = (f, set(requirements))

    def get_phrase(self, phrase, things_present):
        phrase = phrase.strip()
        things_present = set(things_present)
        if not phrase in self.phrases:
            return None
        p = self.phrases[phrase]
        if things_present.issuperset(p[1]):
            return p[0]
        return None

    def output(self, text, message_type=0):
        self.game.output(text, message_type)

    """
    XXX Adding these here to see if it makes sense
    """
    """
    Changes "lock" to "a lock", "apple" to "an apple", etc. Note that no article 
    should be added to proper names; store a global list of these somewhere?  
    For now we'll just assume anything starting with upper case is proper. Do not 
    add an article to plural nouns.
    """
    def add_article(self, name):
        # simple plural test
        if len(name) > 1 and name[len(name) - 1] == "s" and name[len(name) - 2] != "s":
            return name
            
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        if name and (name[0] in vowels):
            article = "an "
        elif name and (name[0] in consonants):
            article = "a "
        else:
            article = ""
        return "%s%s" % (article, name)

    """
    XXX Both the actor and location object make use of this function and they both 
    inherit from Base so it sort of makes sense to put it here for now...
    """
    def proper_list_from_dict(self, d):
        names = list(d.keys())
        buf = []
        name_count = len(names)
        for (i, name) in enumerate(names):
            if i != 0:
                buf.append(", " if name_count > 2 else " ")
            if i == name_count - 1 and name_count > 1:
                buf.append("and ")
            buf.append(self.add_article(name))
        return "".join(buf)

    def print_output(self, text, message_type=0):
        print(self.style_text(text, message_type))


    # this makes the text look nice in the terminal... WITH COLORS!
    def style_text(self, text, message_type):
        if True:  # trinket.io
            return text

        if message_type == FEEDBACK:
            text = Colors.FG.pink + text + Colors.reset

        if message_type == TITLE:
            text = Colors.FG.yellow + Colors.BG.blue + "\n" + text + Colors.reset

        if message_type == DESCRIPTION:
            text = Colors.reset + text

        if message_type == CONTENTS:
            text = Colors.FG.green + text + Colors.reset

        return text

