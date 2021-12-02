import pandas as pd
from robin_stocks import robinhood

ticker = input("Enter ticker :")

df_options = pd.read_csv('completed_options.csv')
df_positions = pd.read_csv('open_positions.csv')
df_stocks = pd.read_csv('completed_stocks.csv')


# options short position calculations
df_filtered_short_positions = df_options[(df_options['opening_strategy'] != 'long_put') & (df_options['opening_strategy'] != 'long_call') & (
        df_options['closing_strategy'] != 'long_put') & (df_options['closing_strategy'] != 'long_call')]
df_filtered_short_positions_instrument = df_filtered_short_positions[
    df_filtered_short_positions['chain_symbol'] == ticker.upper()]
df_filtered_short_positions_instrument_credit = df_filtered_short_positions_instrument[
    df_filtered_short_positions_instrument['direction'] == 'credit']
df_filtered_short_positions_instrument_debit = df_filtered_short_positions_instrument[
    df_filtered_short_positions_instrument['direction'] == 'debit']

df_filtered_short_positions_instrument_credit['total_price_credit'] = df_filtered_short_positions_instrument_credit[
                                                                          'price'] * \
                                                                      df_filtered_short_positions_instrument_credit[
                                                                          'processed_quantity']
df_filtered_short_positions_instrument_debit['total_price_debit'] = df_filtered_short_positions_instrument_debit[
                                                                        'price'] * \
                                                                    df_filtered_short_positions_instrument_debit[
                                                                        'processed_quantity']
total_credit_options = df_filtered_short_positions_instrument_credit['total_price_credit'].sum() * 100
total_debit_options = df_filtered_short_positions_instrument_debit['total_price_debit'].sum() * 100


# average stock price
df_stocks_filtered_ticker = df_stocks[
    df_stocks['symbol'] == ticker.upper()]

df_stocks_filtered_ticker_buy = df_stocks_filtered_ticker[df_stocks_filtered_ticker['side'] == 'buy']

df_stocks_filtered_ticker_sell = df_stocks_filtered_ticker[df_stocks_filtered_ticker['side'] == 'sell']

df_stocks_filtered_ticker_buy['total_price_debit'] = df_stocks_filtered_ticker_buy['average_price'] * df_stocks_filtered_ticker_buy['quantity']

df_stocks_filtered_ticker_sell['total_price_credit'] = df_stocks_filtered_ticker_sell['average_price'] * df_stocks_filtered_ticker_sell['quantity']

total_debit_stocks = df_stocks_filtered_ticker_buy['total_price_debit'].sum()
total_stocks_bought = df_stocks_filtered_ticker_buy['quantity'].sum()

total_credit_stocks = df_stocks_filtered_ticker_sell['total_price_credit'].sum()


# # open positions calculations
# df_filtered_open_position = df_positions[df_positions['symbol'] == ticker.upper()]
# if len(df_filtered_open_position) > 0:
#     total_cost_of_owning_ticker = \
#         (df_filtered_open_position['average_price'] * df_filtered_open_position['quantity']).values[0]
# else:
#     total_cost_of_owning_ticker = None

pnl_options_selling = total_credit_options - total_debit_options
pnl_stocks = total_credit_stocks - total_debit_stocks
average_cost_stock = total_debit_stocks / total_stocks_bought

print('****')
print('Total P/L on %s: %f' % (ticker.upper(), pnl_options_selling+pnl_stocks))
print('P/L from selling options on %s: %f' % (ticker.upper(), pnl_options_selling))
print('P/L from stocks on %s: %f' % (ticker.upper(), pnl_stocks))
print('Average cost of owning %s: %f' % (ticker.upper(), (average_cost_stock)))
print('Average cost of owning(with option selling) %s: %f' % (ticker.upper(), (average_cost_stock*100-pnl_options_selling)/100))
print('****')
