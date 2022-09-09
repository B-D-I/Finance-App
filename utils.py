import datetime as dt
from dateutil import relativedelta
import pandas_datareader as web
from pandas_datareader.yahoo.headers import DEFAULT_HEADERS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import pickle
import requests
import math
import requests_cache
import json
import sqlite3
from sqlite3 import Error as sqlError
from typing import Union
from pandas_datareader.yahoo.headers import DEFAULT_HEADERS
import requests_cache
import typer
from secret import IEX_CLOUD_API_TOKEN

stocks = pd.read_csv('sp_500_stocks.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC', 'VIAC', 'WLTW'])]


def return_date_difference(start: dt, end: dt):
    # return the difference in months, between two dates
    diff = relativedelta.relativedelta(start, end)
    diff_in_months = diff.months + diff.years * 12
    return abs(diff_in_months)


def format_number(number):
    return f'{number:,}'


def return_datetime(date: str):
    # convert string to datetime DD-MM-YY
    try:
        if date == 'now':
            dt_date = dt.datetime.now()
        else:
            dt_date = dt.datetime.strptime(date, "%d-%m-%y")
        return dt_date
    except ValueError or KeyError as error:
        print('Incorrect format', error)


def chunks(lst, n):
    # yield successive n-sized chunks from lst, for batch api calls
    for x in range(0, len(lst), n):
        yield lst[x:x + n]


def return_ticker_array():
    ticker_groups = list(chunks(stocks['Ticker'], 100))
    ticker_array = []
    for x in range(0, len(ticker_groups)):
        ticker_array.append(','.join(ticker_groups[x]))
    return ticker_array
