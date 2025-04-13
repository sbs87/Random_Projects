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
import requests
from flask import Flask, render_template_string
import threading
from datetime import datetime

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


# def calculate_volume_change(data):
#     volume_change = data['Volume'].pct_change() * 100
#     return volume_change


def fetch_stock_info(tickers, short_period='5m', long_period='1d', short_interval='1m', long_interval='1d'):
    stock_info_list = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Fetch historical data for a short (e.g., 5 mins) vs long time (e.g. 1 day) for realtive vol
        hist_short = stock.history(period=short_period, interval=short_interval)
        hist_long = stock.history(period=long_period, interval=long_interval)

        stock_info_list.append({
            'Stock Symbol': ticker,
            'Market Cap': info.get('marketCap', 'N/A'),
            'Float': info.get('floatShares', 'N/A'),
            'Price of Share': info.get('regularMarketPrice', 'N/A'),
            'Volume Traded (Last 5 Min)': hist_short['Volume'].sum() if not hist_short.empty else 'N/A',
            'Volume Traded (Last Day)': hist_long['Volume'].iloc[0] if not hist_long.empty else 'N/A'
        })

    stock_info_df = pd.DataFrame(stock_info_list)
    return stock_info_df


# def main(tickers, interval=60):
#     while True:
#         try:
#             # Fetch and rank stocks by volume change
#             #ranked_stocks = rank_stocks_by_volume_change(tickers)
#             #print("Ranked Stocks by Volume Change:")
#             #print(ranked_stocks)

#             # Fetch stock information
#             stock_info_table = fetch_stock_info(tickers)
#             #print("Stock Information Table:")
#             print(stock_info_table)

#             # Wait for the specified interval before the next iteration
#             time.sleep(interval)
#         except KeyboardInterrupt:
#             print("Monitoring stopped by user.")
#             break
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             break

def main(tickers, interval=60):
    global latest_data
    threading.Thread(target=run_web_server, daemon=True).start()
    while True:
        try:
            stock_info_table = fetch_stock_info(tickers)
            latest_data = stock_info_table
            print(latest_data)
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    app = Flask(__name__)
    latest_data = pd.DataFrame()  # Initialize as an empty DataFrame

    @app.route("/")
    def index():
        global latest_data
        global interval
        #TODO add a way to parametrize "refresh" content
        if latest_data is not None and not latest_data.empty:
            last_updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template_string("""
                <html>
                    <head>
                        <title>Stock Scanner</title>
                        <meta http-equiv="refresh" content="5">
                                          
                    </head>
                    <body>
                        <h1>Stock Information</h1>
                        <p>Last Updated: {{ last_updated_time }}, updating every X SECONDS</p>
                        <p>Time interval: {{ additional_info }}</p>
                        {{ table | safe }}
                    </body>
                </html>
            """, table=latest_data.to_html(index=False), additional_info=interval, last_updated_time=last_updated_time)
        else:
            return "No data available yet."

    def run_web_server():
        app.run(debug=False, use_reloader=False)


    main(nasdaq_tickers, interval=interval)
    # You can set how often the page reloads by modifying the `content` attribute in the meta tag
    # inside the `render_template_string` function in the `index()` route.

    # For example, to change the reload interval to 10 seconds, update this line:
    # <meta http-equiv="refresh" content="5">
    # to:
    # <meta http-equiv="refresh" content="10">
    