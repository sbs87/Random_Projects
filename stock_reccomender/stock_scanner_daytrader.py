# stock_scanner_daytrader.py
# Author: Steve Smith
# Email: sbs@stevenbsmith.net
# Date: 2025-04

# This script scans  stock stats at a specified interval and ranks them by various metrics
# Example usage:
# python stock_scanner_daytrader.py --tickers AAPL MSFT GOOG --interval 60

import time
import yfinance as yf
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Stock Scanner for Day Traders")
parser.add_argument(
        '--tickers', 
        type=str, 
        nargs='+', 
        required=True, 
        help="List of stock tickers to monitor (e.g., AAPL MSFT GOOG)"
)
parser.add_argument(
        '--interval', 
        type=int, 
        default=60, 
        help="Time interval (in seconds) for monitoring stocks"
)
args = parser.parse_args()
interval = args.interval
nasdaq_tickers = args.tickers

def fetch_stock_data(ticker, period, interval):
    stock_data = yf.download(ticker, period=period, interval=interval)
    return stock_data


def calculate_volume_change(data):
    volume_change = data['Volume'].pct_change() * 100
    return volume_change


def fetch_stock_info(tickers):
    stock_info_list = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Fetch historical data for the last 5 minutes and last day
        hist_5m = stock.history(period="5m", interval="1m")
        hist_1d = stock.history(period="1d", interval="1d")

        stock_info_list.append({
            'Stock Symbol': ticker,
            'Market Cap': info.get('marketCap', 'N/A'),
            'Float': info.get('floatShares', 'N/A'),
            'Price of Share': info.get('regularMarketPrice', 'N/A'),
            'Volume Traded (Last 5 Min)': hist_5m['Volume'].sum() if not hist_5m.empty else 'N/A',
            'Volume Traded (Last Day)': hist_1d['Volume'].iloc[0] if not hist_1d.empty else 'N/A'
        })

    stock_info_df = pd.DataFrame(stock_info_list)
    return stock_info_df


def rank_stocks_by_volume_change(tickers, period='5d', interval='1m'):
    stock_data_list = []

    for ticker in tickers:
        stock_data = fetch_stock_data(ticker, period=period, interval=interval)
        if not stock_data.empty:
            stock_data['% Volume Change'] = calculate_volume_change(stock_data)
            latest_volume_change = stock_data['% Volume Change'].iloc[-1]
            stock_data_list.append({'Ticker': ticker, '% Volume Change': latest_volume_change})

    ranked_stocks = pd.DataFrame(stock_data_list).sort_values(by='% Volume Change', ascending=False)
    return ranked_stocks



def monitor_stocks(tickers, interval=60):
    while True:
        try:
            # Fetch and rank stocks by volume change
            ranked_stocks = rank_stocks_by_volume_change(tickers)
            #print("Ranked Stocks by Volume Change:")
            #print(ranked_stocks)

            # Fetch stock information
            stock_info_table = fetch_stock_info(tickers)
            #print("Stock Information Table:")
            print(stock_info_table)

            # Wait for the specified interval before the next iteration
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Example usage:
#nasdaq_tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']  # Replace with a full list of NASDAQ tickers
#ranked_stocks = rank_stocks_by_volume_change(nasdaq_tickers, period='5d', interval='1m'))
#print(ranked_stocks)

# Example usage:
monitor_stocks(nasdaq_tickers, interval=interval)  # Run every 5 minutes