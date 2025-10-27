from trading_view_scrapping import *

if __name__ == '__main__':
    load_dotenv()

    # DATABASE CREDENTIALS
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # VARIABLES
    lookback = int(os.getenv("historic_lookback"))
        
    expmonths = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V','X', 'Z']
    tables_names = {
        'ZC': 'CBOT_corn',
        'CCM': 'B3_corn',
        'ZS': 'CBOT_soybean',
        'ZL': 'CBOT_soybean_oil',
        'ZM': 'CBOT_soybean_meal',
        'BGI': 'B3_live_cattle',
        'ZQ': 'US_ZQ',
        'DX': 'US_DXY',
        'DI1': 'BR_DI1',
        'DOL': 'BR_DOL'
    }

    # Execute the main function
    database_save_data(
        symbols = ['ZC', 'CCM', 'ZS', 'ZL', 'ZM', 'BGI'] + ['ZQ', 'DX', 'DI1', 'DOL'],
        tables_names=tables_names,
        futures_expire_months=expmonths,
        historic_lookback=lookback
    )