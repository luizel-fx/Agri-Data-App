from price_loaders.tradingview import load_asset_price
from datetime import datetime
from dotenv import load_dotenv

import pandas as pd
# Import tqdm for the loading bar
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import text

import os
import pytz

def market_year_flag(exp_year, exp_month):
    my_beg = 'U'  # To these commodities, the market-year starts at 01-September
    my_end = 'Q'  # and ends at 31-Aug.
    
    if (exp_month >= my_beg):
        return f'{exp_year}/{str(exp_year+1)[-2:]}'
    elif (exp_month <= my_end):

        return f'{exp_year-1}/{str(exp_year)[-2:]}'


def tv_scrapping(symbol: str, expire_months: list, init_year: int, lookback: int):
    """
        Scraps TradingView data using the load_asset_price function from price_loaders package.

        Args
        -----
        asset_name: str - Prefix string for the futures contracts of the underlying asset;
        expire_months: list - A list with the expire months available;
        init_year: int - Initial year;
        period: int - How many days of each contracs will be storaged;
        lookback: int - How many expire years will be storaged.

        Returns
        --------
        pd.DataFrame with columns:
            time: date;
            expire_month: str;
            expire_year: int;
            open: float;
            high: float;
            low; float;
            close; float

            if it's a agricultural commodity asset, it'll also have a colums...
                market-year: str.

    """
    dfs = []
    
    # Calculate total number of contracts to scrap for the progress bar
    total_iterations = lookback * len(expire_months)
    
    # Wrap the outermost loop with tqdm to show the progress of all contracts
    with tqdm(total=total_iterations, desc=f"Scraping {symbol} Contracts") as pbar:
        for i in range(lookback):
            for m in expire_months:
                ticker = f'{symbol}{m}{init_year-i}'
                
                try:
                    df = load_asset_price(ticker, 10000, 'D', timezone = pytz.timezone("America/Sao_Paulo"))
                    
                    if df.empty: 
                        pbar.write(f'No data for {ticker}')
                    else:
                        df['time'] = df['time'].apply(lambda x: datetime(x.year, x.month, x.day))
                        df['exp_month'] = m
                        df['exp_year'] = init_year-i

                        if symbol in ['ZC', 'CCM', 'ZS', 'ZL', 'ZM', 'BGI']:
                            df['market_year'] = market_year_flag(init_year-i, m)
                        
                        dfs.append(df)
                        pbar.write(f"Succesfully scrapped data from {ticker}")

                except Exception as e:
                    pbar.write(f"Error scrapping data for {ticker}: {e}") 
                
                pbar.update(1)
                
    scrap = pd.concat(dfs)
    common_cols = ['time', 'exp_month', 'exp_year', 'open', 'high', 'low', 'close']
    if symbol in ['ZC', 'CCM', 'ZS', 'ZL', 'ZM', 'BGI']:
        return scrap[common_cols + ['market_year']]
    else:
        return scrap[common_cols]

def database_save_data(symbols: list, tables_names: dict, futures_expire_months: list, historic_lookback: int):
    engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/futures_db")
    con = engine.connect()
    init_year = datetime.now().year + 1
    
    for symbol in tqdm(symbols, desc="Overall Asset Progress"):
        df = tv_scrapping(symbol, expire_months=futures_expire_months, init_year=init_year, lookback=historic_lookback)
        
        tqdm.write(f"Saving data for {symbol} to table {tables_names[symbol].lower()}...")
        df.to_sql(name = tables_names[symbol].lower(), con = con, if_exists = 'replace', index=False)
        tqdm.write(f"Finished saving data for {symbol}.")