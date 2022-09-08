from database import *

"""
Portfolio Functions:
- create ring chart of user's portfolio
"""


def display_portfolio_data(tickers: list[str], ticker_amounts: list[int], start: dt, end: dt):
    """
    :param tickers: company stock symbol
    :param ticker_amounts: amount invested in each company
    :param start: start date: dt.datetime(YYYY-MM-DD)
    :param end: end date: dt.datetime(YYYY-MM-DD) or .now()
    :return: call portfolio ring chart function
    """
    for ticker in tickers:
        df = web.DataReader(ticker, 'yahoo', start, end)
        price = df[-1:]['Close'][0]
        prices.append(price)
        index = tickers.index(ticker)
        total.append(price * ticker_amounts[index])

    portfolio_ring_chart(tickers)


def portfolio_ring_chart(tickers: list[str]):
    # figure size and customisation
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    ax.figure.set_facecolor('black')
    ax.tick_params(axis='x', color='white')
    ax.tick_params(axis='y', color='white')
    ax.set_title('Portfolio', color='white', fontsize=22)
    # customise labels
    _, texts, _ = ax.pie(total, labels=tickers, autopct='%1.1f%%', pctdistance=0.8)
    [text.set_color('white') for text in texts]
    # black out middle of chart
    my_circle = plt.Circle((0, 0), 0.65, color='black')
    plt.gca().add_artist(my_circle)
    # display portfolio data inside chart
    ax.text(0, 0.35, f'Total USD Amount: {sum(total):.2f} $', fontsize=11, color='white',
            verticalalignment='center', horizontalalignment='center')
    counter = 0.15
    # display ticker values inside chart
    for ticker in tickers:
        ax.text(0, 0.35 - counter, f'{ticker}: {total[tickers.index(ticker)]:.2f}$', fontsize=12, color='white',
                verticalalignment='center', horizontalalignment='center')
        counter += 0.15
    plt.show()