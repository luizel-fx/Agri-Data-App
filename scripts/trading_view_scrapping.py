from price_loaders.tradingview import load_asset_price
from datetime import datetime
from dotenv import load_dotenv
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
        ------
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
    for i in range(lookback):
        for m in expmonths:
            ticker = f'{symbol}{m}{init_year-i}'
            try:
                df = load_asset_price(ticker, lookback, 'D', timezone = pytz.timezone("America/Sao_Paulo"))
                if df.empty: print(f'No data for {ticker}')

                df['time'] = df['time'].apply(lambda x: datetime(x.year, x.month, x.day))
                df['exp_month'] = m
                df['exp_year'] = init_year-i

                if symbol in ag_symbols:
                    df['market_year'] = market_year_flag(init_year-i, m)
                dfs.append(df)

            except Exception as e:
                print(f"Error scrapping data for {ticker}: {e}") 
    scrap = pd.concat(dfs)
    common_cols = ['time', 'exp_month', 'exp_year', 'open', 'high', 'low', 'close']
    if symbol in ag_symbols:
        return scrap[common_cols + ['market_year']]
    else:
        return scrap[common_cols]


if __name__ == '__main__':
    load_dotenv()
    init_year = datetime.now().dt.year + 1
    lookback = os.getenv("historic_lookback")
    expmonths = os.getenv("futures_expire_months")
    ag_symbols = os.getenv('ag_symbols')