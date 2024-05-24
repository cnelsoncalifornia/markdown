from otree.api import *

doc = """
Comprehension test. If the user fails too many times, they exit.
"""


class C(BaseConstants):
    NAME_IN_URL = 'directions_test'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MAX_FAILED_ATTEMPTS = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)
    independent = models.StringField(
        choices=[['Yes', 'Yes'], ['No', 'No']],
        label='Does the performance of one asset influence the performance of any other asset?',
        widget=widgets.RadioSelect,
    )
    bid_question1 = models.IntegerField(
        label='If you bid 15 and the random number is 11, what price do you pay for the asset?'
    )
    bid_question2 = models.StringField(
        choices=[['Yes', 'Yes'], ['No', 'No']],
        label='Do you purchase the asset if you bid 5 and the random number is 8?',
        widget=widgets.RadioSelect,
    )
    prob_question1 = models.IntegerField(
        label='''
        If an asset has increased 3 periods in a row, what is the chance that 
        it will increase next period?  Enter as a percentage.''',
        min=0, max=100
    )
    prob_question2 = models.IntegerField(
        label='''
        If an asset has decreased 6 periods in a row, what is the chance that it will decrease next period?  
        Enter as a percentage.''',
        min=0, max=100
    )
    payoff_question = models.StringField(
        choices=[['True', 'True'], ['False', 'False']],
        label='True or False: The payoff of any asset is unknown until the 10th period of the round.',
        widget=widgets.RadioSelect,
    )


class Directions(Page):
    pass


class MyPage(Page):
    form_model = 'player'
    form_fields = ['independent', 'bid_question1', 'bid_question2', 'prob_question1', 'prob_question2', 'payoff_question']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(independent='No', bid_question1=11, bid_question2='No', prob_question1=50, prob_question2=50,
                         payoff_question='True')

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {name: 'Wrong' for name in solutions if values[name] != solutions[name]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= C.MAX_FAILED_ATTEMPTS:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'failed' page that boots them
                # from the experiment.
            else:
                return errors


class Failed(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many


class Results(Page):
    pass


page_sequence = [Directions, MyPage, Failed, Results]