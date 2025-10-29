from datetime import datetime
import pandas as pd
from statsmodels.tsa.stattools import coint

import torch
from torch.autograd import Variable

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

def min_max_scaler(serie):
    min = serie.min()
    max = serie.max()
    return (serie - min)/(max - min)

def normalized_spread_serie(con, symbol, exp_month, exp_year):
    ticker = data_loader(con, symbol, exp_month, exp_year)[['time', 'close']]
    ticker['norm'] = min_max_scaler(ticker['close'])
    return ticker[['time','norm']]

def cs_coint_data(con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year, hist_period):
    coint_data_dfs = [] 
    for i in range(1, hist_period+1):
        long_norm_data = normalized_spread_serie(con, symbol=symbol, exp_month=long_exp_month, exp_year=long_exp_year-i)
        short_norm_data = normalized_spread_serie(con, symbol=symbol, exp_month=short_exp_month, exp_year=short_exp_year-i)

        year_norm_dfs = long_norm_data.merge(short_norm_data, on = 'time', how = 'inner', suffixes=('long', 'short'))[-252:]
        coint_data_dfs.append(year_norm_dfs)

    return pd.concat(coint_data_dfs)

def cs_coint_test(con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year, hist_period):
    data = cs_coint_data(con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year, hist_period)
    return coint(data['normlong'], data['normshort'])

def load_and_align_now_data(con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year):
    # Carrega a data de vencimento LONGA (long_exp)
    long_df = data_loader(con=con, symbol=symbol, exp_month=long_exp_month, exp_year=long_exp_year)
    long_df = long_df[['time', 'close']].rename(columns={'close': 'long_close'})

    # Carrega a data de vencimento CURTA (short_exp)
    short_df = data_loader(con=con, symbol=symbol, exp_month=short_exp_month, exp_year=short_exp_year)
    short_df = short_df[['time', 'close']].rename(columns={'close': 'short_close'})

    # Faz o merge usando 'time' (data/hora) para garantir que apenas os 
    # pontos de dados sobrepostos (datas presentes em ambos) sejam incluídos.
    aligned_now_data = long_df.merge(
        short_df, 
        on='time', 
        how='inner' # Use 'inner' para garantir sobreposição total
    )[-252:]
    
    # Retorna as duas séries de preços alinhadas
    return aligned_now_data['long_close'], aligned_now_data['short_close']

import matplotlib.pyplot as plt
def cs_coint_model(con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year, hist_period):
    train_data = cs_coint_data(con, symbol, long_exp_month, short_exp_month, long_exp_year - 1, short_exp_year - 1, round(hist_period*0.7))
    test_data = cs_coint_data(con, symbol, long_exp_month, short_exp_month, long_exp_year - 1, short_exp_year - 1, hist_period - round(hist_period*0.7))
    
    now_long_close, now_short_close = load_and_align_now_data(
        con, symbol, long_exp_month, short_exp_month, long_exp_year, short_exp_year
    )
    
    # --- MODEL CREATION (Corrected) ---
    class LinearRegression(torch.nn.Module):
        def __init__(self, n_in_feat, n_out_feat):
            super(LinearRegression, self).__init__()
            self.linear = torch.nn.Linear(n_in_feat, n_out_feat)
        def forward(self, x):
            return self.linear(x)
    
    model = LinearRegression(1, 1)
    lr = 0.1
    criterion = torch.nn.MSELoss() 
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    
    X_train = torch.from_numpy(train_data['normlong'].values).float().unsqueeze(1)
    y_train = torch.from_numpy(train_data['normshort'].values).float().unsqueeze(1)
    
    for epoch in range(200):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

    # --- INFERENCE & PLOTTING ---
    with torch.no_grad():
        # 1. Test Data Residuals (The main metric)
        test_input = torch.from_numpy(test_data['normlong'].values).float().unsqueeze(1)
        test_y_pred = model(test_input).data.squeeze().numpy() 
        test_resid = test_y_pred - test_data['normshort'].values # Use .values to ensure NumPy array subtraction

        now_input_tensor = torch.from_numpy(now_long_close.values).float().unsqueeze(1) 
        now_y_pred = model(now_input_tensor).data.squeeze().numpy() 
        
        now_resid = now_short_close.values - now_y_pred
    
    #plt.scatter(x = now_input_tensor, y = now_short_close.values)
    plt.scatter(x = test_input, y = test_data['normshort'].values)
    plt.show()

if __name__ == '__main__':
    from dotenv import load_dotenv


    import os
    import sys

    load_dotenv()
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from src.data_access.data_loader import data_loader
    from src.data_access.database_connector import db_connector

    # DATABASE CREDENTIALS
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    con = db_connector(DB_USER, DB_PASSWORD)
    print(cs_coint_model(con, 'CCM', 'F', 'K', 2026, 2026, 5))