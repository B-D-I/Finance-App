from stock_analysis import *
from portfolio_options import *


def get_stock_data_menu():
    ticker = input('Enter Company Ticker: ')
    data_response = input("""

    To View All Response Options Enter: A
    To Quit Enter: Q

    Enter Response Attribute:
    """)
    if data_response == 'A' or data_response == 'a':
        print(return_iex_api_options(ticker))
        get_stock_data_menu()
    elif data_response == 'Q' or data_response == 'q':
        user_menu()
    else:
        try:
            print(return_iex_data(ticker, data_response))
        except json.JSONDecodeError as error:
            print('Error: ', error)
        finally:
            get_stock_data_menu()


def return_datetime(date: str):
    try:
        if date == 'now':
            dt_date = dt.datetime.now()
        else:
            dt_date = dt.datetime.strptime(date, "%d-%m-%y")
        return dt_date
    except ValueError or KeyError as error:
        print('Incorrect format', error)
        candlestick_volume_chart_menu()


def time_series_options():
    ticker = input('Enter Company Ticker or Quit (Q): ')
    start = input('Enter Start Date: (DD-MM-YY)')
    end = input('Enter End Date: (DD-MM-YY) (for now enter: now)')
    start = return_datetime(start)
    end = return_datetime(end)
    ticker_options = [ticker, start, end]
    return ticker_options


def rsi_menu():
    ticker_selection = time_series_options()
    rsi_analysis(ticker_selection[0], ticker_selection[1], ticker_selection[2])


def candlestick_volume_chart_menu():
    ticker_selection = time_series_options()
    ticker = ticker_selection[0]
    moving_av = input('Include Moving Averages? (Y/N): ').upper()
    if ticker == 'Q' or ticker == 'q':
        user_menu()
    else:
        if moving_av == 'Y' or moving_av == 'YES':
            start_month = int(input('Enter number for starting month: '))
            display_timeseries_candlestick_data(ticker, ticker_selection[1], ticker_selection[2], True, start_month)
        else:
            display_timeseries_candlestick_data(ticker, ticker_selection[1], ticker_selection[2], False)


def stock_analysis_menu():
    command = input("""

    Select Option or Quit (Q):

    1. Retrieve Company Stock Data

    2. Display Candlestick Timeseries and Volume

    3. Display Candlestick Timeseries and Relative Strength Index
    """)
    if command == '1':
        get_stock_data_menu()
    elif command == '2':
        candlestick_volume_chart_menu()
    elif command == '3':
        rsi_menu()
    elif command == 'Q' or command == 'q':
        user_menu()


def user_menu():
    while True:
        command = input("""

        *** Financial Assistant ***

        Select Option:

        1. View Market Summary

        2. View Portfolio

        3. Update Portfolio 
        """)
        if command == '1':
            stock_analysis_menu()
        elif command == '2':
            # use sql data
            display_portfolio_data(['AAPL', 'TSLA', 'FB', 'AMZN', 'GOOG'], [8, 2, 2, 5, 7],
                                   dt.datetime(2022, 1, 20), dt.datetime.now())
        elif command == '3':
            # update portfolio
            pass
        else:
            user_menu()



