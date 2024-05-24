from otree.api import *

doc = """
Comprehension test. If the user fails too many times, they exit.
"""


class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Consent(Page):
    pass



page_sequence = [Consent]