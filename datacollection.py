from robin_stocks import robinhood
from csv import writer
import pandas as pd

password = input ("Enter password :")
robinhood.login(username='ali.muhammadimran@gmail.com', password=password)

robinhood.export.export_completed_option_orders('.', 'completed_options.csv')
robinhood.export.export_completed_stock_orders('.', 'completed_stocks.csv')

# add option assignment information to the completed_stocks.csv
event_rows = []
df_stocks = pd.read_csv('completed_stocks.csv')
ticker_list = list(df_stocks['symbol'].unique())
for ticker in ticker_list:
    events = robinhood.get_events(ticker)
    for event in events:
        event_row = [ticker, event['event_date'], event['type'], 'buy' if event['direction'] == 'debit' else 'sell',
                     '0.00', float(event['quantity']) * 100, float(event['total_cash_amount']) / 100]
        event_rows.append(event_row)

with open('completed_stocks.csv', 'a', newline='') as f:
    csv_writer = writer(f)
    for event_row in event_rows:
        csv_writer.writerow(event_row)
    f.close()






