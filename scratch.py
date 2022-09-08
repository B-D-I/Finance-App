import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
from utils import *
import bs4 as bs
import requests
import pickle

"""
Unused / Not complete functions 
"""


def chunks(lst, n):
    # yield successive n-sized chunks from lst, for batch api calls
    for x in range(0, len(lst), n):
        yield lst[x:x + n]


def return_ticker_df():
    # add stocks data to data frame
    ticker_dataframe = pd.DataFrame(columns=ticker_columns)
    return ticker_dataframe


def return_ticker_array():
    df = return_ticker_df()
    ticker_groups = list(chunks(stocks['Ticker'], 100))
    ticker_array = []
    for x in range(0, len(ticker_groups)):
        ticker_array.append(','.join(ticker_groups[x]))
    return ticker_array


def return_batch_api_ticker_data():
    ticker_array = return_ticker_array()
    for ticker in ticker_array:
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={ticker}&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        # remove comma and append all ticker data to dataframe
        for t in ticker.split(','):
            df = return_ticker_df().append(
                pd.Series([ticker,
                           data[ticker]['quote']['latestPrice'],
                           data[ticker]['quote']['marketCap']
                           ],
                          index=ticker_columns),
                ignore_index=True)
        return df

def old_show_candlestick_data(ticker):
    start = dt.datetime(2022, 5, 1)
    end = dt.datetime.now()
    # load data (company ticker symbol, finance api, start, end)
    data_original = web.DataReader(ticker, 'yahoo', start, end)
    # USING DEPRECIATED MPL_FINANCE:
    # restructure data
    data = data_original[['Open', 'High', 'Low', 'Close']]
    # take all dates and convert to number format
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].map(mdates.date2num)
    # visualise
    ax = plt.subplot()
    # add grid
    ax.grid(True)
    # set grid in background
    ax.set_axisbelow(True)
    # set title
    ax.set_title(f'{ticker} Share Price', color='white')
    # set background colour
    ax.set_facecolor('black')
    # set window background colour
    ax.figure.set_facecolor('#121212')
    # set tick colour
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    # x-axis is used for dates
    ax.xaxis_date()

    candlestick_ohlc(ax, data.values, width=0.5, colorup='#00ff00')
    # plt.show()


# S&P webscrape
html = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text, features='lxml')

tickers = []
table = soup.find('table', {'class': 'wikitable sortable'})
# ignore first row
rows = table.findAll('tr')[1:]
for row in rows:
    ticker = row.findAll('td')[0].text
    # append and remove last 2 chars
    tickers.append(ticker[:-1])

# create pickle of ticker array
with open('snp500.pickle', 'wb') as f:
    pickle.dump(tickers, f)


def get_snp500_ticker():
    with open('snp500.pickle', 'rb') as f:
        ticker_array = pickle.load(f)
    return ticker_array


# ticker batch api calls
ticker_columns = ['Ticker', 'Stock Price', 'Market Capitalization']






