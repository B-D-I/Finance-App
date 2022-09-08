from user_menu import *

# TO DO:
# create sqlite database of stock portfolio -> functions to perform analysis
# multithreading -> start a separate thead to retrieve stock data
# unit testing
# security -> create secure login


if __name__ == '__main__':
    user_menu()

    # print(return_iex_data('AAPL', 'latestPrice'))

    # display_timeseries_candlestick_data('AAPL', dt.datetime(2022, 1, 20), dt.datetime.now(), True, 55)

    # display_portfolio_data(['AAPL', 'TSLA', 'FB', 'AMZN', 'GOOG'], [8, 2, 2, 5, 7],
    #                        dt.datetime(2022, 1, 20), dt.datetime.now())

    # rsi_analysis('AAPL', dt.datetime(2022, 1, 20), dt.datetime.now())