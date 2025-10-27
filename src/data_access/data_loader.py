from database_connector import *
import pandas as pd
from datetime import datetime

def data_loader(con, symbol, exp_month, exp_year):
    tables = {
        'ZC':  'CBOT_corn',
        'CCM': 'B3_corn',
        'ZS':  'CBOT_soybean',
        'ZL':  'CBOT_soybean_oil',
        'ZM':  'CBOT_soybean_meal',
        'BGI': 'B3_live_cattle',
        'ZQ':  'US_ZQ',
        'DX':  'US_DXY',
        'DI1': 'BR_DI1',
        'DOL': 'BR_DOL'
        }

    table = tables[symbol]
    query = f"""
        SELECT * from {table}
            WHERE 
                (exp_month = '{exp_month}' AND
                exp_year = {exp_year})
    """
    return pd.read_sql(query, con = con)

def date_adjustment(df, i):
    try: df = df[~((df['time'].dt.month == 2) & (df['time'].dt.day == 29))] # # Dropping the 29-Feb of the leap year.
    except: pass
    df['time'] = df['time'].apply(lambda x: datetime(x.year + i, x.month, x.day))
    return df

def calendar_spread_df(con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year, hist_period):
    for i in range(hist_period):
        long_ticker = data_loader(con = con, symbol = symbol, exp_month=long_exp_month, exp_year=long_exp_year-i)
        long_ticker = date_adjustment(long_ticker, i)[['time', 'close']]

        short_ticker = data_loader(con = con, symbol = symbol, exp_month=short_exp_month, exp_year=short_exp_year-i)
        short_ticker = date_adjustment(short_ticker, i)[['time', 'close']]

        long_suffix = f'_{long_exp_month}{long_exp_year-i}'
        short_suffix = f'_{short_exp_month}{short_exp_year-i}'

        col_name = f'{long_exp_month}{long_exp_year-i} - {short_exp_month}{short_exp_year-i}'
        if i == 0:
            # First iteration - create the base dataframe
            merged_spread_df = long_ticker.merge(short_ticker, how = 'left', on = 'time', suffixes=(long_suffix, short_suffix))
            merged_spread_df[col_name] = merged_spread_df[f'close{long_suffix}'] - merged_spread_df[f'close{short_suffix}']
            merged_spread_df = merged_spread_df[['time', col_name]]
        else:
            # Subsequent iterations - merge with existing dataframe
            spread_df = long_ticker.merge(short_ticker, how = 'left', on = 'time', suffixes=(long_suffix, short_suffix))
            spread_df[col_name] = spread_df[f'close{long_suffix}'] - spread_df[f'close{short_suffix}']
            spread_df = spread_df[['time', col_name]]
            merged_spread_df = merged_spread_df.merge(spread_df, on = 'time', how = 'outer')
    
    return merged_spread_df

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    load_dotenv()

    # DATABASE CREDENTIALS
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


    con = db_connector(DB_USER, DB_PASSWORD)
    print(calendar_spread_df(con, 'ZS', 'N', 'X', 2025, 2025, 5))