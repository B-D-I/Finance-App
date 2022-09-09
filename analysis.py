from api_requests import *
from data_visualisation import *

visualisation = Visualisations()
database = Database()
api = IEXStocks(IEX_CLOUD_API_TOKEN)


def create_rsi_df(rsi: pd.Series, df: pd.DataFrame):
    # create data frame to plot results
    combined = pd.DataFrame()
    combined['Adj Close'] = df['Adj Close']
    combined['RSI'] = rsi
    index = combined.index
    visualisation.display_rsi_chart(index, combined['Adj Close'], combined['RSI'])


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
    session = Database.create_and_return_cache(ticker, start, 'RSI')
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


def return_portfolio_data(data_type):
    portfolio = database.get_all_table_data('portfolio')
    ticker_list = []
    for ticker in portfolio:
        if data_type == 'tickers':
            ticker_list.append(ticker[1])
        elif data_type == 'shares':
            ticker_list.append(ticker[2])
    return ticker_list

