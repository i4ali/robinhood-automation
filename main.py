import pandas as pd

ticker = input("Enter ticker :")

df = pd.read_csv('completed_options.csv')
df3 = pd.read_csv('open_positions.csv')

# options short position calculations
df_filtered_short_positions = df[(df['opening_strategy'] != 'long_put') & (df['opening_strategy'] != 'long_call') & (
        df['closing_strategy'] != 'long_put') & (df['closing_strategy'] != 'long_call')]
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
total_credit = df_filtered_short_positions_instrument_credit['total_price_credit'].sum() * 100
total_debit = df_filtered_short_positions_instrument_debit['total_price_debit'].sum() * 100

# open positions calculations
df_filtered_open_position = df3[df3['symbol'] == ticker.upper()]
if len(df_filtered_open_position) > 0:
    total_cost_of_owning_ticker = \
        (df_filtered_open_position['average_price'] * df_filtered_open_position['quantity']).values[0]
else:
    total_cost_of_owning_ticker = None

pnl_options_selling = total_credit - total_debit

print('****')
print('P/L from selling options on %s: %s' % (ticker.upper(), pnl_options_selling))
if total_cost_of_owning_ticker:
    print('Average cost of owning %s (without option selling): %s' % (ticker.upper(), total_cost_of_owning_ticker))
    print('Average cost of owning %s: %s' % (ticker.upper(), (total_cost_of_owning_ticker - pnl_options_selling)))
print('****')
