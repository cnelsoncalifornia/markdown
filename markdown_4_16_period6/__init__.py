from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'markdown_4_16_period6'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    MAX = 20 # Maximum bid.
    NAMES = {
        1: ['K', 'C'],  # First (highest) asset in market 1, second asset in market 2.
        2: ['M', 'B'],
        3: ['L', 'G'],
        4: ['L', 'D']
    }

    PROJ_PAYOFF_6 = { # Projected payoffs in period 3.
        1: {'K': 4, 'C': 16},
        2: {'M': 10, 'B': 14},
        3: {'L': 8, 'G': 12},
        4: {'L': 6, 'D': 10}
    }

    PAYOFFS = {
        1: {'K': 6, 'C': 16},
        2: {'M': 10, 'B': 16},
        3: {'L':8, 'G': 14},
        4: {'L':4, 'D': 8}
    }



class Subsession(BaseSubsession):
    cummulative_earnings = models.IntegerField(initial = 0)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bid_6 = models.IntegerField(label='', min=0, max=C.MAX)
    bid_6_2 = models.IntegerField(label='', min=0, max=C.MAX)
    price_6 = models.IntegerField(initial = 0)
    price_6_2 = models.IntegerField(initial = 0)
    curr_payoff_6 = models.IntegerField(initial = 0) # Projected payoff after period 3 of first asset.
    curr_payoff_6_2 = models.IntegerField(initial = 0)
    shares_acquired_6 = models.IntegerField(initial=0)  # Shares acquired in the first purchase after period 3.
    shares_acquired_6_2 = models.IntegerField(initial=0)  # Shares acquired in the second purchase after period 3.
    acquired_6 = models.StringField(initial = 'No') # Yes if shares_aquired_6 is 1, otherwise No.
    acquired_6_2 = models.StringField(initial = 'No') # Yes if shares_aquired_6_2 is 1, otherwise No.
    payoff_6 = models.IntegerField(initial=0) # Payoff for the first asset purchased after round 3.
    payoff_6_2 = models.IntegerField(initial=0)  # Payoff for the second asset purchased after round 3.
    earnings_6 = models.IntegerField(initial=0)  # payoff_6 * shares_acquired_6 - price_6
    earnings_6_2 = models.IntegerField(initial=0)  # payoff_6_2 * shares_acquired_6_2 - price_6_2
    guess_6 = models.IntegerField(label='', min=0, max=C.MAX)  # Subject's guess for the final payout of the first asset they bid on in the first market.
    guess_6_2 = models.IntegerField(label='', min=0, max=C.MAX)



    earnings = models.IntegerField(initial=0) # Earnings for the round from asset payoffs.
    earnings_1 = models.IntegerField(initial=0) # Total earnings from the first market.
    earnings_from_guess_1 = models.IntegerField(initial=0)  # Earnings from correct payoff guesses in the first round. +/- 1 is okay.

    asset_6 = models.StringField(initial='') # Name of tne first (highest) asset that could be picked at the end of round 3.
    asset_6_2 = models.StringField(initial='') # Name of the second asset that could be picked at the end of round 3.

    cummulative_earnings = models.IntegerField(initial=0)



# FUNCTIONS
# PAGES
class Intro(Page):
    def vars_for_template(player: Player):
        if (player.subsession.session.config['first_session'] == 3) and (player.round_number == 1): # This app is the first.
            player.participant.vars['round'] = 0
            player.participant.vars['cummulative_earnings'] = 0

        current_round = player.round_number + player.participant.vars['round'] 
        if player.round_number == C.NUM_ROUNDS:
            player.participant.vars['round'] += C.NUM_ROUNDS

        return{
            'current_round': current_round
        }




class Bid1(Page):

    def vars_for_template(player: Player):
       player.asset_6 = C.NAMES[player.round_number][0]  # The name of the first asset that can be purchased after period 3.
       player.asset_6_2 = C.NAMES[player.round_number][1] # The name of the second asset that can be purchased after period 3.

       player.payoff_6 = C.PAYOFFS[player.round_number][player.asset_6]  # The payoff of the first asset that can be purchased after period 3.
       player.payoff_6_2 = C.PAYOFFS[player.round_number][player.asset_6_2]  # The payoff of the second asset that can be purchased after period 3.

       player.curr_payoff_6 = C.PROJ_PAYOFF_6[player.round_number][player.asset_6]
       player.curr_payoff_6_2 = C.PROJ_PAYOFF_6[player.round_number][player.asset_6_2]

       return dict(
          image_path1= 'markdown_4_16_period6/markdown_{}_period6.jpg'.format(player.round_number),
          image_path2='markdown_4_16_period6/markdown_{}_graph.jpg'.format(player.round_number),

       )
    form_model = 'player'
    form_fields = ['guess_6','guess_6_2','bid_6','bid_6_2']




class Results1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        ran_int = random.randint(1,C.MAX)
        purchase_6 = (ran_int<=player.bid_6)

        if purchase_6:
            player.price_6 = ran_int
            player.shares_acquired_6 = 1
            player.acquired_6 = "Yes"
            statement = "Since " + str(ran_int) +" is less than or equal to your first bid, you puchased 1 unit of asset " + player.asset_6 + " at the price of " + str(player.price_6) +"."
        else:
            player.shares_acquired_6 = 0
            statement = "Since " + str(ran_int) + " is greater than your first bid, you did not purchase any units of asset " + player.asset_6 + "."

        ran_int_2 = random.randint(1,C.MAX)
        purchase_6_2 = (ran_int_2<=player.bid_6_2)

        if purchase_6_2:
            player.price_6_2 = ran_int_2
            player.shares_acquired_6_2 = 1
            player.acquired_6_2 = "Yes"
            statement_2 = "Since " + str(ran_int_2) +" is less than or equal to your second bid, you puchased 1 unit of asset " + player.asset_6_2 + " at the price of " + str(player.price_6_2) +"."
        else:
            player.shares_acquired_6_2 = 0
            statement_2 = "Since " + str(ran_int_2) + " is greater than your second bid, you did not purchase any units of asset " + player.asset_6_2 + "."

        return{
            "ran_int":ran_int,
            "statement":statement,
            "ran_int_2":ran_int_2,
            "statement_2":statement_2,
        }







class CombinedResults(Page):
    @staticmethod
    def vars_for_template(player: Player):

        player.earnings_6 = player.payoff_6 * player.shares_acquired_6 - player.price_6
        player.earnings_6_2 = player.payoff_6_2 * player.shares_acquired_6_2 - player.price_6_2

        player.earnings_from_guess_1 = 0

        if abs(player.guess_6 - player.payoff_6) == 0:
            player.earnings_from_guess_1 += 1
        if abs(player.guess_6_2 - player.payoff_6_2) == 0:
            player.earnings_from_guess_1 += 1

        player.earnings = player.earnings_6 + player.earnings_6_2 + player.earnings_from_guess_1

        player.participant.vars['cummulative_earnings'] += player.earnings

        player.cummulative_earnings = player.participant.vars['cummulative_earnings']



        return dict(
            image_path= 'markdown_4_16_period6/markdown_{}_final.jpg'.format(player.round_number)
        )

page_sequence = [Intro, Bid1 , Results1, CombinedResults]
