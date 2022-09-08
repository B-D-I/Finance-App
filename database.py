from utils import *

"""
Database Functions:
- create cache of api queries 
- return user / portfolio data  
"""


def create_and_return_cache(ticker: str, start: dt, reference: str):
    """
    Provide an SQLite cache of query
    :param ticker: ticker name
    :param start: start date
    :param reference: further reference for naming
    :return: cached session
    """
    cache_expire_after = dt.timedelta(days=3)
    session = requests_cache.CachedSession(cache_name=f'{ticker}_{reference}_{str(start.date())}', backend='sqlite',
                                           expire_after=cache_expire_after)
    session.headers = DEFAULT_HEADERS
    return session