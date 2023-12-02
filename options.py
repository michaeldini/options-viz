from matplotlib import pyplot as plt
import numpy as np
import yfinance as yf
import pandas as pd


def gather_option_data(ticker: str):

    stock = yf.Ticker(ticker)
    expirys = stock.options

    volume_puts = []
    open_interest_puts = []
    volume_calls = []
    open_interest_calls = []

    for expiry_date in expirys[:4]:
        chain = stock.option_chain(expiry_date)

        puts = chain.puts.set_index('strike')
        volume_puts.append(puts['volume'].rename('volume_' + expiry_date))
        open_interest_puts.append(
            puts['openInterest'].rename('openInterest_' + expiry_date))

        calls = chain.calls.set_index('strike')
        volume_calls.append(calls['volume'].rename('volume_' + expiry_date))
        open_interest_calls.append(
            calls['openInterest'].rename('openInterest_' + expiry_date))

    data = {
        'volume_puts': pd.concat(volume_puts, axis=1).sort_index(),
        'open_interest_puts': pd.concat(open_interest_puts, axis=1).sort_index(),
        'volume_calls': pd.concat(volume_calls, axis=1).sort_index(),
        'open_interest_calls': pd.concat(open_interest_calls, axis=1).sort_index(),
    }
    return data


def visualize_options(ticker: str, data: dict):
    for title, df in data.items():
        df.replace(0, np.nan).plot(title=title, figsize=(
            14, 8))
        plt.savefig(f'{ticker}_{title}.png')


if __name__ == "__main__":
    ticker = "MSFT".upper()
    data = gather_option_data(ticker)
    visualize_options(ticker, data)
