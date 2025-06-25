# This script reads a TSV file containing stock order data output from DayTrade_Analysis.ipynb, transforms it into a specific JSON format, and writes the output to a JSON file.
# The input file is expected to have columns: Datetime, Open, High, Low, Close and be tsv-delimited.

import csv
import json
from datetime import datetime
import argparse
import os
# Set up argument parsing
parser = argparse.ArgumentParser(description='Transform stock order data from TSV to JSON format.',usage="""python3  convert_stock_hx_to_json.py --input_file /Users/stevensmith/Documents/Other/Financials/Day_trade_stocks/yfinance/stock_order_2025-06-03_MCTR_1m.tsv --output_file stock_order_2025-06-03_MCTR_1m.json
or (omit output_file to use default name):
python3  convert_stock_hx_to_json.py --input_file /Users/stevensmith/Documents/Other/Financials/Day_trade_stocks/yfinance/stock_order_2025-06-06_VERO_1m.tsv""")
parser.add_argument('--input_file', type=str, help='Path to the input TSV file')
parser.add_argument('--output_file', type=str, help='Path to the output JSON file. If none is provided, uses input file prefix name (+ local path)',required=False, default=None)
args = parser.parse_args()  
#TODO: by default, use basename and prefix for output json. Override with --output_file

input_file = args.input_file
output_file = args.output_file

if output_file is None:
    # If no output file is specified, use the input file name with a .json extension
    output_file = os.path.splitext(os.path.basename(input_file))[0] + '.json'

# Read the TSV file and transform the data
# Note the time is in Unix seconds which will be correctly read in to Lightweight Charts (e.g., 1 min charts). 
# The tutorial has daily charts, which would be in the format 'YYYY-MM-DD', but we are using 1 min charts. 
transformed_data = []
with open(input_file, mode='r', encoding='utf-8') as tsv_file:
    tsv_reader = csv.DictReader(tsv_file, delimiter='\t')
    for row in tsv_reader:
        timestamp = int(datetime.strptime(row['Datetime'], "%Y-%m-%d %H:%M:%S%z").timestamp())
        transformed_data.append({
            "time": timestamp,
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
        })

# Write the transformed data to the JSON file. This is consumed by lightweight-charts as the data source.
with open(output_file, mode='w', encoding='utf-8') as json_file:
    json.dump(transformed_data, json_file, indent=4)

print(f"json file created: {output_file}")


order_csv_path = '/Users/stevensmith/Projects/Random_Projects/day_trading/data/raw_data/order_hx/Webull_Order_Records_2025_06_16.csv'  # Path to the order summary CSV file
output_json_path = "/Users/stevensmith/Projects/Random_Projects/day_trading/src/Lightweight_Charts/foo.json"
# Additional section: Convert order summary CSV to filtered JSON
def convert_order_summary_to_json(order_csv_path, output_json_path):
    filtered_orders = []
    with open(order_csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if (row.get('Status', '').strip().lower() == 'filled') and row.get('Symbol', '').strip()=="VERO":
                dt_str = row['Filled Time'].replace("EDT", "").strip()
                dt_obj = datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S")
                dt_obj = dt_obj.replace(tzinfo=None)
                timestamp = int(datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S").timestamp())
                timestamp = timestamp - (timestamp % 60)

                # # Convert 'Datetime' like '2025-06-06 09:30:00-04:00' to unix timestamp
                # if '-' in row['Datetime'] and ':' in row['Datetime']:
                # dt_obj = datetime.strptime(row['Datetime'], "%Y-%m-%d %H:%M:%S%z")
                # timestamp = int(dt_obj.timestamp())
                if row['Side'] == 'Buy':
                    output_color = "#FFA200"
                if row['Side'] == 'Sell':
                    output_color = "#0055FF"
                filtered_orders.append({
                    "symbol": row['Symbol'],
                    "time": timestamp,
                    "num_shares" : row['Filled'],
                    "buy_sell": row['Side'],
                    "color": output_color,
                    "value": float(row['Avg Price'])
                })
    with open(output_json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(filtered_orders, json_file, indent=4)
    print(f"Filtered order summary JSON created: {output_json_path}")
convert_order_summary_to_json(order_csv_path, output_json_path)
# Example usage:
# convert_order_summary_to_json('order_summary.csv', 'order_summary_filtered.json')
#Datetime Symbol,  Side,    Status,  Filled , AvgPrice               Time-in-Force   PlacedTime      FilledTime      Date    Time    UID     Total_Price   


