import os
import pandas as pd

df = pd.read_csv("rawdata/yahoo_stocks/_BATCH_TSLA/TSLA.csv")
# df["ts"] = pd.to_datetime(df["ts"])
# df["ts"] = df["ts"].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
print(df.columns)
