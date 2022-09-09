from analysis import *
from api_requests import *
from data_visualisation import *
from threading import Thread

visual = Visualisations()
api = IEXStocks(IEX_CLOUD_API_TOKEN)

app = typer.Typer()
threads = []


@app.command()
def return_company_info(ticker: str, data_type: str):
    """
    This function will return specified company information, and create a separate thread
    to return call the get_api_data function and receive the latest price
    :param ticker: company ticker symbol
    :param data_type: required data (example: totalCash). Type 'options' for api dictionary
    :return: api request data
    """
    thread = Thread(target=get_api_data, args=[ticker, 'latestPrice'])
    thread.start()
    threads.append(thread)

    data = api.get_stats(ticker)
    if data_type == 'options':
        return data
    else:
        return data[data_type]


@app.command()
def get_api_data(ticker: str, data_type: str):
    """
    :param ticker: company ticker symbol
    :param data_type: required data (example: latestPrice). Type 'options' for api dictionary
    :return: api request data
    """
    data = api.get_quote(ticker)
    if data_type == 'options':
        return data
    else:
        print(data[data_type])


@app.command()
def display_candlestick_timeseries(ticker: str, start: dt, end: dt, is_moving_average: bool, *mv_av_start: int):
    """
    Display OHLC candlestick timeseries chart with volume graph. Optional moving average and start month
    Example Params: ('AAPL', dt.datetime(2022, 1, 20), dt.datetime.now(), True, 5)
    :param ticker: company ticker symbol
    :param start: start date: dt.datetime(YYYY-MM-DD)
    :param end: end date: dt.datetime(YYYY-MM-DD)
    :param is_moving_average: boolean, include moving average
    :return: candlestick share price chart
    """
    visual.display_timeseries_candlestick_data(ticker, start, end, is_moving_average, *mv_av_start)


@app.command()
def display_rsi_and_candlestick(ticker: str, start: dt, end: dt):
    """
    Display candlestick timeseries chart with Relative Strength Index volume indicator
    :param ticker: company ticker symbol
    :param start: start date: dt.datetime(YYYY-MM-DD)
    :param end: end date: dt.datetime(YYYY-MM-DD)
    :return: candlestick share price chart with RSI oscillator
    """
    rsi_analysis(ticker, start, end)


@app.command()
def display_portfolio_data():
    """
    Retrieve portfolio data from database, then display ring chart & data
    :return: ring chart
    """
    tickers = return_portfolio_data('tickers')
    ticker_amounts = return_portfolio_data('shares')
    for ticker in tickers:
        df = web.DataReader(ticker, 'yahoo')
        # get closing price of ticker -> append to prices[] -> give ticker an index
        price = df[-1:]['Close'][0]
        prices.append(price)
        index = tickers.index(ticker)
        # append to total[] the closing price of ticker * times the amount of shares
        total.append(price * ticker_amounts[index])
    visualisation.portfolio_ring_chart(tickers, total)


@app.command()
def update_portfolio(ticker: str, share_amount: int):
    try:
        database.update_db('portfolio', 'share_amount', share_amount, 'ticker_name', ticker)
    except ValueError as error:
        print(error)


@app.command()
def insert_to_portfolio(ticker: str, share_amount: int):
    try:
        database.insert_db('portfolio', ticker, share_amount)
    except ValueError as error:
        print(error)


if __name__ == '__main__':
    # app()
    apple_total_cash = return_company_info('AAPL', 'totalCash')
    print(format_number(apple_total_cash))



