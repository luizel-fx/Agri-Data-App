#from database_connector import *
import pandas as pd

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

#if __name__ == '__main__':
#    from dotenv import load_dotenv
#    import os
#
#    load_dotenv()#
#
#    # DATABASE CREDENTIALS
#    DB_USER = os.getenv("DB_USER")
#    DB_PASSWORD = os.getenv("DB_PASSWORD")

#    con = db_connector(DB_USER, DB_PASSWORD)