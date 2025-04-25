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
        '--market_cap_upper_threshold', 
        type=float, 
        required=False, 
        default=1E8,
        help="Market cap upper threshold for filtering stocks. Default 1E8"
)
parser.add_argument(
        '--market_cap_lower_threshold', 
        type=float, 
        required=False, 
        default=10,
        help="Market cap lower threshold for filtering stocks. Default 10"
)
parser.add_argument(
        '--interval', 
        type=int, 
        default=60, 
        help="Time interval (in seconds) for monitoring stocks"
)
args = parser.parse_args()
interval = args.interval
market_cap_upper_threshold = args.market_cap_upper_threshold
market_cap_lower_threshold = args.market_cap_lower_threshold

def fetch_stock_data(ticker, period, interval):
    stock_data = yf.download(ticker, period=period, interval=interval)
    return stock_data


# def calculate_volume_change(data):
#     volume_change = data['Volume'].pct_change() * 100
#     return volume_change

#TODO read in list of tickers at once - cycling through ~1000 symbols is way to slow
# Can do this using yf.download([list]); however the result needs to be re-formatted
def fetch_stock_info(tickers, short_period='5m', long_period='1d', short_interval='1m', long_interval='1d'):
    stock_info_list = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Fetch historical data for a short (e.g., 5 mins) vs long time (e.g. 1 day) for realtive vol
        hist_short = stock.history(period=short_period, interval=short_interval)
        hist_long = stock.history(period=long_period, interval=long_interval)

        stock_info_list.append({
            'Symbol': ticker,
            'MarketCap': info.get('marketCap', 'N/A'),
            'Float': info.get('floatShares', 'N/A'),
            'Price': info.get('regularMarketPrice', 'N/A'),
            'ShortTerm_Volume': hist_short['Volume'].sum() if not hist_short.empty else 'N/A',
            'LongTerm_Volume': hist_long['Volume'].iloc[0] if not hist_long.empty else 'N/A',
            'RSI': "FUTURE_FEATURE",
            'VWAP': "FUTURE_FEATURE"
        })

    stock_info_df = pd.DataFrame(stock_info_list)
    return stock_info_df

def sort_stock_info(stock_table):
    stock_table['relative_volume'] = stock_table['ShortTerm_Volume'].replace("N/A",0) / stock_table['LongTerm_Volume'].replace("N/A",0) 
    sorted_stock_table = stock_table.sort_values(by='relative_volume', ascending=False)
    return sorted_stock_table


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

# Loads stock ticker symbols from a CSV file and filters them based on market cap
def load_filter_tickers(infile, market_cap_upper_threshold, market_cap_lower_threshold):
    
    static_cols = ["Symbol", "Name", "Market Cap", "IPO Year", "Sector", "Industry"]
    ticker_df =   pd.read_csv(infile)
    ticker_df_subcols = ticker_df[static_cols]
    ticker_df_subcols_filter = ticker_df_subcols[(ticker_df_subcols['Market Cap'] < market_cap_upper_threshold) & (ticker_df_subcols['Market Cap'] > market_cap_lower_threshold) ][0:5]

    print(f"Number of symbols at {market_cap_upper_threshold} - {market_cap_lower_threshold}: {ticker_df_subcols_filter.shape}")

    return ticker_df_subcols_filter["Symbol"].to_list(), ticker_df_subcols_filter


def main(tickers, interval=60):
    global latest_data
    threading.Thread(target=run_web_server, daemon=True).start()
    while True:
        try:
            stock_info_table = fetch_stock_info(tickers)
            latest_data = sort_stock_info(stock_info_table)
            #latest_data = stock_info_table
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
    fromfile = False

    # load tickers by market cap
    if fromfile:
        nasdaq_tickers, nasdaq_tickers_df = load_filter_tickers(infile="~/Downloads/nasdaq_screener_1744643468853.csv",market_cap_upper_threshold=market_cap_upper_threshold, market_cap_lower_threshold=market_cap_lower_threshold)
    else:
        nasdaq_tickers = ["OMH","SNOA"]
        nasdaq_tickers_df=pd.DataFrame()

    
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

    