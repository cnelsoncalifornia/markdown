from os import environ
import random
#import sys
#from termcolor import colored



#This code block is to clear cache.
import requests
from requests.structures import CaseInsensitiveDict

url = "https://reqbin.com/echo"

headers = CaseInsensitiveDict()
headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
headers["Pragma"] = "no-cache"
headers["Expires"] = "0"

resp = requests.get(url, headers=headers)
#End clear cache code block.

ss_first = round(random.randint(0,1))  # This variable is changed at random.  It determines which app comes first.


#ss_first = 1    # Put 1 if you want superstars to come first

app_1 = ""
app_2 = ""
app_1_practice = ""
app_2_practice = ""
if ss_first == 1:
    app_1 = 'asset_experiment_cliff_nelson'                 # Superstar assets are possible in this app.
    app_2 = 'asset_experiment_cliff_nelson_no_superstars'   # Superstar assets are not possible in this app.
    app_1_practice = 'practice_superstars'
    app_2_practice = 'practice_no_superstars'
    print("Superstars.")
elif ss_first == 0:
    app_1 = 'asset_experiment_cliff_nelson_no_superstars'
    app_2 = 'asset_experiment_cliff_nelson'
    app_1_practice = 'practice_no_superstars'
    app_2_practice = 'practice_superstars'
    print("No superstars.")



numbers = [0, 1, 2, 3]
random.shuffle(numbers)
print(numbers)

markdown = ['markdown_10_period3', 'markdown_10_period6', 'markdown_7_13_period3', 'markdown_4_16_period6']

first_session = numbers[0]



SESSION_CONFIGS = [
    dict(
        name='asset_experiment_cliff_nelson',
        display_name="Asset Experiment",
        app_sequence=['markdown_consent', 'markdown_directions', 'markdown_practice', markdown[numbers[0]], markdown[numbers[1]], markdown[numbers[2]], markdown[numbers[3]], 'markdown_conclusion'],                  # ['consent_form', 'directions', app_1_practice, app_2_practice, app_1, app_2, 'asset_experiment_cliff_nelson_7_13', 'final_instructions'], #   'loss_firms',
        num_demo_participants=20,
        ss_first=ss_first,
        first_session = first_session,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'round',
    'final_earnings',
    'final_earnings_app2',
    'final_earnings_bonus',
    'cummulative_earnings',
    'app_first',
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True



SECRET_KEY = '7829773786560'

INSTALLED_APPS = ['otree']

