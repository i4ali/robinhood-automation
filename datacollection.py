from robin_stocks import robinhood
from csv import writer

password = input ("Enter password :")
robinhood.login(username='ali.muhammadimran@gmail.com', password=password)

robinhood.export.export_completed_option_orders('.', 'completed_options.csv')
robinhood.export.export_completed_stock_orders('.', 'completed_stocks.csv')
all_orders = robinhood.account.build_holdings(with_dividends=False)
with open('open_positions.csv', 'w', newline='') as f:
    csv_writer = writer(f)
    csv_writer.writerow([
        'symbol',
        'average_price',
        'quantity'
    ])
    for symbol, data in all_orders.items():
        csv_writer.writerow([
            symbol,
            data['average_buy_price'],
            data['quantity'],
        ])
    f.close()

