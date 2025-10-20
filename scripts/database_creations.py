from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import text

# Importing database credentials
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def create_database(DB_USER, DB_PASSWORD):
    engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/futures_db")
    if not database_exists(engine.url):
        create_database(engine.url)

    con = engine.connect()
    return con

def table_creation(con, table_name, symbol):
    ag_tables_colnames = """
        time DATE,
        exp_month VARCHAR(1),
        exp_year INTEGER,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        market_year VARCHAR(7),

        PRIMARY KEY (time, exp_month, exp_year)
    """

    macro_tables_colnames = """
    time DATE,
    exp_month VARCHAR(1),
    exp_year INTEGER,
    open REAL,
    high REAL,
    low REAL,
    close REAL,

    PRIMARY KEY (time, exp_month, exp_year)
    """
    if symbol in ['ZC', 'CCM', 'ZS', 'ZL', 'ZM', 'BGI']: columns = ag_tables_colnames
    else: columns = macro_tables_colnames

    con.execute(text(f"CREATE TABLE IF NOT EXISTS {table_name}({columns})"))

def create_tables(CON):
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

    for symbol in tables.keys():
        symbol_table = tables[symbol]
        table_creation(CON, symbol_table, symbol)

if __name__ == '__main__':
    CON = create_database(DB_USER, DB_PASSWORD)
    create_tables(CON)
