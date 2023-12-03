from matplotlib import pyplot as plt
import numpy as np
import yfinance as yf
import pandas as pd


def gather_option_data(ticker: str):

    # gather stock data
    stock = yf.Ticker(ticker)
    expiry_dates = stock.options
    current_price = stock.info['currentPrice']

    # use these lists to hold options data
    # will concat the list into a df later
    volume_puts = []
    open_interest_puts = []
    volume_calls = []
    open_interest_calls = []

    for expiry_date in expiry_dates[:5]:

        # get option chain (puts & calls) for given date
        chain = stock.option_chain(expiry_date)

        # get and append the puts data (df)
        # label columns with expiry data
        puts = chain.puts.set_index('strike')
        volume_puts.append(puts['volume'].rename(expiry_date))
        open_interest_puts.append(
            puts['openInterest'].rename(expiry_date))

        # get and append the puts data (df)
        # label columns with expiry data
        calls = chain.calls.set_index('strike')
        volume_calls.append(calls['volume'].rename(expiry_date))
        open_interest_calls.append(
            calls['openInterest'].rename(expiry_date))

    # concat each list. each df has index of strike price and columns for expiry dates
    data = {
        'current_price': current_price,
        'dfs': {
            'volume_puts': pd.concat(volume_puts, axis=1).sort_index(),
            'open_interest_puts': pd.concat(open_interest_puts, axis=1).sort_index(),
            'volume_calls': pd.concat(volume_calls, axis=1).sort_index(),
            'open_interest_calls': pd.concat(open_interest_calls, axis=1).sort_index(),
        }
    }

    return data


def visualize_options(ticker: str, data: dict):
    for title, df in data['dfs'].items():
        df.replace(0, np.nan).plot(title=title, figsize=(
            14, 8))
        plt.savefig(f'{ticker}_{title}.png')


def heatmap_options(ticker, data):
    pass


if __name__ == "__main__":
    # ticker = "MSFT".upper()
    ticker = input(
        "An image file will be saved in the current directory for given ticker.\nEnter a ticker and hit enter: ").upper()
    data = gather_option_data(ticker)
    visualize_options(ticker, data)
    heatmap_options(ticker, data)
