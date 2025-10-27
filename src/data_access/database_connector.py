from sqlalchemy import create_engine

def db_connector(DB_USER, DB_PASSWORD):
    engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/futures_db")
    con = engine.connect()
    return con