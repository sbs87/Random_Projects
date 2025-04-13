import time
import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period, interval):
    stock_data = yf.download(ticker, period=period, interval=interval)
    return stock_data


def calculate_volume_change(data):
    volume_change = data['Volume'].pct_change() * 100
    return volume_change


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
            print("Ranked Stocks by Volume Change:")
            print(ranked_stocks)

            # Fetch stock information
            stock_info_table = fetch_stock_info(tickers)
            print("Stock Information Table:")
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
nasdaq_tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']  # Replace with a full list of NASDAQ tickers
#ranked_stocks = rank_stocks_by_volume_change(nasdaq_tickers, period='5d', interval='1m'))
#print(ranked_stocks)

# Example usage:
monitor_stocks(nasdaq_tickers, interval=30)  # Run every 5 minutes