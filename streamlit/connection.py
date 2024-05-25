import pandas as pd
from pinotdb import connect

conn = connect(host='20.33.33.13', port=8099, path='#/query/sql', scheme='http')

def fetch_places_data(stock_name):
    query = f"""SELECT * FROM {stock_name};"""
    curs = conn.cursor()
    curs.execute(query)
    
    data = curs.fetchall()

    df = pd.DataFrame(data, columns=['symbol', 'ts_str', 'price', 'change', 'day_volume', 'ts'])
    return df

places_df = fetch_places_data("TSLA")
print(places_df)
