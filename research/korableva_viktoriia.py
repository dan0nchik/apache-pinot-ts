# -*- coding: utf-8 -*-
"""Korableva_Viktoriia.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wzOI9HDAjtaJrRkBbNkQ2RHRwK0Bj1LU
"""

!pip install statsmodels
!pip install pmdarima

"""## Imports"""

import pandas as pd
import warnings
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from pmdarima import auto_arima
from sklearn import metrics
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split

"""## Gdrive"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive/')
# %cd /content/drive/MyDrive/NewsStocksData
!ls

"""## Read data & EDA"""

df = pd.read_excel('new.xlsx')

df.head()

df["Adj Close**"].plot(figsize=(15, 6))
 plt.xlabel("Date")
 plt.ylabel("Adj Close**")
 plt.title("Adj Closing price of stocks")
 plt.show()

plt.figure(1, figsize=(15,6))
plt.subplot(211)
df["Adj Close**"].hist()
plt.subplot(212)
df["Adj Close**"].plot(kind='kde')
plt.show()

"""## ADfuller test"""

def timeseries_evaluation_metrics_func(y_true, y_pred):
  def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
  print('Evaluation metric results:-')
  print(f'MSE is : {metrics.mean_squared_error(y_true, y_pred)}')
  print(f'MSE is : {metrics.mean_absolute_error(y_true, y_pred)}')
  print(f'RMSE is : {np.sqrt(metrics.mean_squared_error(y_true, y_pred))}')
  print(f'MAPE is : {mean_absolute_percentage_error(y_true, y_pred)}')
  print(f'R2 is : {metrics.r2_score(y_true, y_pred)}',end='\n\n')

def Augmented_Dickey_Fuller_Test_func(series , column_name):
  print (f'Results of Dickey-Fuller Test for column: {column_name}')
  dftest = adfuller(series, autolag='AIC')
  dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value','No Lags Used','Number of Observations Used'])
  for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value
  print (dfoutput)
  if dftest[1] <= 0.05:
    print("Conclusion:====>")
    print("Reject the null hypothesis")
    print("Data is stationary")
  else:
    print("Conclusion:====>")
    print("Fail to reject the null hypothesis")
    print("Data is non-stationary")

Augmented_Dickey_Fuller_Test_func(df['Adj Close**' ],'Adj Close**')

"""## Fix test size"""

TEST_SIZE = int(len(df)*0.25)

"""#SARIMA"""

from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm

X = df[['Adj Close**']]
X = X.set_index(df['Date'])
X = X.dropna()
train, test = X[0:-TEST_SIZE], X[-TEST_SIZE:]

model = auto_arima(train, start_p=0, start_q=0, max_p=7, max_q=7, seasonal=True,
d=0, trace=True,error_action='ignore',suppress_warnings=True, stepwise=True)
model.summary()
model = model.fit(train)

forecast = model.predict(TEST_SIZE)
forecast = pd.DataFrame(forecast)
forecast = forecast.set_index(test.index)

plt.rcParams["figure.figsize"] = [15, 7]
plt.plot(test, label='Test')
plt.plot(forecast, label='Predicted')
leg = plt.legend(loc='best')
plt.show()

timeseries_evaluation_metrics_func(test, forecast)



"""# ARMA"""

from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(train, order=(1,0,1)).fit()

forecast = model.forecast(TEST_SIZE)
forecast = pd.DataFrame(forecast)
forecast = forecast.set_index(test.index)

plt.rcParams["figure.figsize"] = [15, 7]
plt.plot(test, label='Test')
plt.plot(forecast, label='Predicted')
leg = plt.legend(loc='best')
plt.show()

timeseries_evaluation_metrics_func(test, forecast)

"""#GARCH"""

!pip3 install arch

from sklearn import metrics
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
warnings.filterwarnings("ignore")
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import yfinance as yf

import statsmodels.api as sm
import arch
from statsmodels.compat import lzip

import matplotlib.pyplot as plt

from arch import arch_model
from sklearn.model_selection import train_test_split

df['returns'] = df['Adj Close**'].pct_change()*100
df.head()

df.dropna(inplace = True)
df.head()

plt.figure(figsize=(12,8))
df['returns'].plot()
plt.title('Daily returns for stocks from 2018 to 2023')
plt.show()

print(f'Mean of Daily Returns = {df.returns.mean()}')

plot_pacf(df['returns']**2)
plt.show()

split_size = int(len(df)*0.3)
X = df[['returns']]
train, test = X[0:-split_size], X[-split_size:]

model = arch.arch_model(train, mean='Zero', vol = 'GARCH', p = 1, q = 1, rescale = False)
results = model.fit(disp='off',show_warning = False)
residuals = results.resid
squared_residuals = residuals**2
conditional_variances = results.conditional_volatility ** 2
mse = np.mean((squared_residuals - conditional_variances) ** 2)
print(f'Mean Squared Error: {mse}')
arch_test = sm.stats.diagnostic.het_arch(squared_residuals)
print(f'ARCH test results:\n')
print(f'LM Statistic: {arch_test[0]}')
print(f'p-value: {arch_test[1]}')
print(f'F Statistic: {arch_test[2]}')
print(f'p-value: {arch_test[3]}')

rolling_predictions = []
test_size = int(len(df)*0.3)

returns = df['returns']

for i in range(test_size):
    train = returns[:-(test_size-i)]
    model = arch_model(train, mean='Zero', vol = 'GARCH', p = 1, q = 1, rescale = False)
    model_fit = model.fit(disp='off', show_warning = False)
    pred = model_fit.forecast(horizon=1)
    rolling_predictions.append(np.sqrt(pred.variance.values[-1,:][0]))

rolling_predictions = pd.Series(rolling_predictions, index=returns.index[-test_size:])

plt.figure(figsize=(10,4))
true, = plt.plot(returns[-test_size:])
preds, = plt.plot(rolling_predictions)
plt.title('Volatility Prediction - Rolling Forecast', fontsize=20)
plt.legend(['True Returns', 'Predicted Volatility'], fontsize=16)

"""# RNNs

Testing RNN on randomply formed dataset
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Generate a simple time-series data
def generate_time_series(batch_size, n_steps):
    freq1, freq2, offsets1, offsets2 = np.random.rand(4, batch_size, 1)
    time = np.linspace(0, 1, n_steps)
    series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10))
    series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20))
    series += 0.1 * (np.random.rand(batch_size, n_steps) - 0.5)
    return series[..., np.newaxis]

# Prepare the data
n_steps = 50
series = generate_time_series(10000, n_steps + 1)
X_train, y_train = series[:7000, :n_steps], series[:7000, -1]
X_valid, y_valid = series[7000:9000, :n_steps], series[7000:9000, -1]
X_test, y_test = series[9000:, :n_steps], series[9000:, -1]

# Build the LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(n_steps, 1)),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=20, validation_data=(X_valid, y_valid))

# Predict future values
y_pred = model.predict(X_test)

import matplotlib.pyplot as plt

# Select a segment of the test data to visualize
n_visualize = 100  # Number of steps to visualize

# Actual vs. Predicted plot
plt.figure(figsize=(10, 6))
plt.plot(y_test[:n_visualize], marker='o', label='Actual', linestyle='-', color='r')
plt.plot(y_pred[:n_visualize], marker='x', label='Predicted', linestyle='--', color='b')
plt.title('Actual vs. Predicted')
plt.xlabel('Time Steps')
plt.ylabel('Value')
plt.legend()
plt.show()

# Calculate the MSE
mse = np.mean(np.square(y_pred.squeeze() - y_test.squeeze()))

print(f'Mean Squared Error (MSE) on Test Set: {mse}')

"""## Testing RNN on provided dataset"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense



# Assuming 'Adj Close**' is what we want to predict, let's normalize this column
scaler = MinMaxScaler(feature_range=(0, 1))
df['Adj Close**'] = scaler.fit_transform(df[['Adj Close**']].values)

# Function to create sequences
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# Prepare the data
look_back = 1
data = df['Adj Close**'].values
data = data.reshape(-1, 1)

# Split into train and test sets
train_size = int(len(data) * 0.67)
test_size = len(data) - train_size
train, test = data[0:train_size,:], data[train_size:len(data),:]

# Reshape into X=t and Y=t+1
X_train, Y_train = create_dataset(train, look_back)
X_test, Y_test = create_dataset(test, look_back)

# Reshape input to be [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Build the LSTM model
model_lstm = Sequential()
model_lstm.add(LSTM(4, input_shape=(1, look_back)))
model_lstm.add(Dense(1))
model_lstm.compile(loss='mean_squared_error', optimizer='adam')
model_lstm.fit(X_train, Y_train, epochs=100, batch_size=1, verbose=2)

# Make predictions
trainPredict = model_lstm.predict(X_train)
testPredict = model_lstm.predict(X_test)

plt.figure(figsize=(10, 6))

# Plotting the actual vs predicted values
plt.plot(Y_train, label='Actual Train Data')
plt.plot(trainPredict, label='Predicted Train Data')
plt.plot(range(len(Y_train), len(Y_train) + len(Y_test)), Y_test, label='Actual Test Data')
plt.plot(range(len(Y_train), len(Y_train) + len(Y_test)), testPredict, label='Predicted Test Data')

plt.title('LSTM Model - Actual vs Predicted')
plt.xlabel('Time')
plt.ylabel('Values')
plt.legend()
plt.show()

train_mse = mean_squared_error(Y_train, trainPredict)
test_mse = mean_squared_error(Y_test, testPredict)

print(f'Train Mean Squared Error: {train_mse}')
print(f'Test Mean Squared Error: {test_mse}')

"""# APIs for fetching data

## yfinance
"""

!pip install yfinance --upgrade --no-cache-dir
import yfinance as yf

ticker = yf.Ticker("AAPL")

info = ticker.info
print("Company Name:", info['shortName'])
print("Sector:", info['sector'])
print("Full time employees:", info['fullTimeEmployees'])

history = ticker.history(period="1mo")
print(history)

dividends = ticker.dividends
print(dividends)

"""## yahoo_fin"""

!pip install yahoo_fin

import os
from yahoo_fin.stock_info import get_data
import pandas as pd
from datetime import datetime

def fetch_stock_data(ticker_name):
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    base_dir = f"rawdata/yahoo_stocks/{ticker_name}"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    try:
        data = get_data(ticker_name)

        if data.empty:
            print(f"No data available for {ticker_name} on {today_date}")
            return

        file_path = os.path.join(base_dir, f"{ticker_name}.csv")
        data.to_csv(file_path)
    except Exception as e:
        print(f"Error fetching data for {ticker_name}: {e}")


list_tickers = ["AMZN", "AAPL", "DELL","LULU"]

for ticker in list_tickers:
    fetch_stock_data(ticker)

# для быстрого удаления папок
import shutil
import os

directory_path = "rawdata/yahoo_stocks"

if os.path.exists(directory_path):
    shutil.rmtree(directory_path)
    print(f"Directory {directory_path} has been removed")
else:
    print("Directory does not exist")

"""##Quandl"""

!pip install quandl
import quandl as quandl

quandl.ApiConfig.api_key = 'nyjwpgHMctUs1UJy-pi6'
mydata = quandl.get("FRED/GDP", start_date="2020-12-31", end_date="2023-9-26")
mydata

"""# WebSocket

getting real-time data from Yahoo Finance
"""

!pip install websockets

from ticker_pb2 import Ticker # из загружаемого файла
import base64
import json
import websockets

def deserialize(message):
    ticker_ = Ticker()
    message_bytes = base64.b64decode(message)
    ticker_.ParseFromString(message_bytes)
    return (ticker_.id, ticker_)

import json
from websocket import create_connection

ticker_list = ['AMZN']

def yf_input(worker_tickers):
    ws = create_connection("wss://streamer.finance.yahoo.com/")
    ws.send(json.dumps({"subscribe": worker_tickers}))
    while True:
        result = ws.recv()
        print(deserialize(result))
        yield result

# Example:
for message in yf_input(ticker_list):
    pass