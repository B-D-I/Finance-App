import datetime as dt
from dateutil import relativedelta
import pandas_datareader as web
from pandas_datareader.yahoo.headers import DEFAULT_HEADERS
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import pickle
import requests
import math
import requests_cache
from secret import IEX_CLOUD_API_TOKEN
import json

prices = []
total = []
stocks = pd.read_csv('sp_500_stocks.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC', 'VIAC', 'WLTW'])]
