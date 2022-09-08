from database import *

"""
Stock Analysis Functions:
- return_iex_ticker_data: returns specified data regarding ticker
- display_timeseries_candlestick_data: display candlestick and volume indicator chart
                            of specified ticker and dates. Includes optional moving average parameter
- rsi analysis: also provides candlestick chart, but with RSI oscillator 
"""


def return_iex_api_json(ticker: str):
    # free version: dummy stocks
    api_url = f'https://sandbox.iexapis.com/stable/stock/{ticker}/quote/?token={IEX_CLOUD_API_TOKEN}'
    # retrieve json dictionary of company information
    data = requests.get(api_url).json()
    return data


def return_iex_api_options(ticker: str):
    data = return_iex_api_json(ticker)
    api_options = [x for x in data.keys()]
    return api_options


def return_iex_data(ticker: str, data_type: str):
    data = return_iex_api_json(ticker)
    return_data = data[data_type]
    return return_data


def return_date_difference(start: dt, end: dt):
    # return the difference in months, between two dates
    diff = relativedelta.relativedelta(start, end)
    diff_in_months = diff.months + diff.years * 12
    return abs(diff_in_months)


def display_timeseries_candlestick_data(ticker: str, start: dt, end: dt, moving_average: bool, *mv_av_start: int):
    """
    :param ticker: company ticker symbol
    :param start: start date: dt.datetime(YYYY-MM-DD)
    :param end: end date: dt.datetime(YYYY-MM-DD)
    :param moving_average: boolean, include moving average
    :return: candlestick share price chart
    """
    session = create_and_return_cache(ticker, start, 'yh')
    df = web.DataReader(ticker, 'yahoo', start, end, session=session)
    colors = mpf.make_marketcolors(up='#1ac949', down='#c9201a', wick='inherit', edge='inherit', volume='in')
    mpf_styles = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
    start_date = str(start)
    end_date = str(end)
    if moving_average:
        mpf.plot(df, type='candle', mav=mv_av_start, style=mpf_styles, title=f'\n{ticker} Share Price: '
                                        f'{start_date[:10]} - {end_date[:10]}\nWith Moving Average', volume=True)
    else:
        mpf.plot(df, type='candle', style=mpf_styles, title=f'{ticker} Share Price: '
                                                            f'{start_date[:10]} - {end_date[:10]}', volume=True)


def display_rsi_chart(index, combined_adj_close, combined_rsi):
    plt.figure(figsize=(12, 8))
    # adj close
    ax1 = plt.subplot(211)
    ax1.plot(index, combined_adj_close, color='white')
    ax1.set_title('Adjusted Close Price', color='white')
    ax1.grid(True, color='#555555')
    ax1.set_axisbelow(True)
    ax1.set_facecolor('black')
    ax1.figure.set_facecolor('black')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    # rsi
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(index, combined_rsi, color='lightgray')
    ax2.axhline(0, linestyle='--', alpha=0.6, color='#ff0000')
    ax2.axhline(10, linestyle='--', alpha=0.6, color='#ffaa00')
    ax2.axhline(20, linestyle='--', alpha=0.6, color='lightgray')
    ax2.axhline(30, linestyle='--', alpha=0.6, color='lightgray')
    ax2.axhline(70, linestyle='--', alpha=0.6, color='lightgray')
    ax2.axhline(80, linestyle='--', alpha=0.6, color='lightgray')
    ax2.axhline(90, linestyle='--', alpha=0.6, color='#ffaa00')
    ax2.axhline(100, linestyle='--', alpha=0.6, color='#ff0000')
    ax2.set_title('RSI Value')
    ax2.grid(False)
    ax2.set_axisbelow(True)
    ax2.set_facecolor('black')
    ax2.figure.set_facecolor('black')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    plt.show()


def create_rsi_df(rsi: pd.Series, df: pd.DataFrame):
    # create data frame to plot results
    combined = pd.DataFrame()
    combined['Adj Close'] = df['Adj Close']
    combined['RSI'] = rsi
    index = combined.index
    display_rsi_chart(index, combined['Adj Close'], combined['RSI'])


def return_rsi_value(positive: pd.Series, negative: pd.Series):
    days = 14
    # get pos values of specified days and get mean > vice versa but remove negative to get difference
    average_gain = positive.rolling(window=days).mean()
    average_loss = abs(negative.rolling(window=days).mean())
    relative_strength = average_gain / average_loss
    # rsi formula
    rsi = 100.0 - (100.0 / (1.0 + relative_strength))
    return rsi


def rsi_analysis(ticker: str, start: dt, end: dt):
    session = create_and_return_cache(ticker, start, 'RSI')
    df = web.DataReader(ticker, 'yahoo', start, end, session=session)
    # calculate the difference from previous -> remove NA values -> then create duplicates
    delta = df['Adj Close'].diff(1)
    delta.dropna(inplace=True)
    positive = delta.copy()
    negative = delta.copy()
    # keep all positives, set all negatives set to 0 > vice versa
    positive[positive < 0] = 0
    negative[negative > 0] = 0
    rsi = return_rsi_value(positive, negative)
    create_rsi_df(rsi, df)