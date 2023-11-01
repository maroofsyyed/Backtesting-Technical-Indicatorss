'''
This python file contains alll the parameters which could be changed for Variations in Historical stock
data and the backtesting parameters
'''

import datetime


START_DATE =datetime.datetime(2023, 6, 1)
TICKER = 'TSLA'
API_KEY = "PKTAPN93MAWDX4EVX1EJ"
SECRET_KEY = "vrJcnbeDoYcHd2RSvSQUzkRrGtjHNztTuEEPHVpQ"
STOP_LOSS_PCT = 0.005
investment = 100000
RISK_FREE_RATE= 3
ANNUALIZE_COEFFICIENT = 98280
EMA_PERIOD = 20