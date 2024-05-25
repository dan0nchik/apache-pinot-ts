import pandas as pd
from pinotdb import connect

conn = connect(host="172.17.0.1", port=8099, path="/query/sql", scheme="http")


def fetch_places_data(stock_name, columns):
    query = f"""SELECT * FROM {stock_name} ORDER BY ts ASC;"""
    curs = conn.cursor()
    curs.execute(query, queryOptions="useMultistageEngine=true")

    data = curs.fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df


def fetch_news():
    query = f"""SELECT * FROM news;"""
    curs = conn.cursor()
    curs.execute(query, queryOptions="useMultistageEngine=true")

    data = curs.fetchall()
    df = pd.DataFrame(data, columns=["entry_json"])
    return df
