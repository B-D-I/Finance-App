from database import *
prices = []
total = []
database = Database()


class Visualisations:

    @staticmethod
    def display_timeseries_candlestick_data(ticker: str, start: dt, end: dt, moving_average: bool, *mv_av_start: int):
        session = database.create_and_return_cache(ticker, start, 'yh')
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

    @staticmethod
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

    @staticmethod
    def portfolio_ring_chart(tickers: list[str], totals: list[int]):
        # figure size and customisation
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_facecolor('black')
        ax.figure.set_facecolor('black')
        ax.tick_params(axis='x', color='white')
        ax.tick_params(axis='y', color='white')
        ax.set_title('Portfolio', color='white', fontsize=22)
        # customise labels
        _, texts, _ = ax.pie(totals, labels=tickers, autopct='%1.1f%%', pctdistance=0.8)
        [text.set_color('white') for text in texts]
        # black out middle of chart
        my_circle = plt.Circle((0, 0), 0.65, color='black')
        plt.gca().add_artist(my_circle)
        # display portfolio data inside chart
        ax.text(0, 0.35, f'Total USD Amount: {sum(totals):.2f} $', fontsize=11, color='white',
                verticalalignment='center', horizontalalignment='center')
        counter = 0.15
        # display ticker values inside chart
        for ticker in tickers:
            ax.text(0, 0.35 - counter, f'{ticker}: {totals[tickers.index(ticker)]:.2f}$', fontsize=12, color='white',
                    verticalalignment='center', horizontalalignment='center')
            counter += 0.15
        plt.show()