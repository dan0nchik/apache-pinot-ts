from datetime import date
import math
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit


def dates(df):
    df["year"] = df["ts"].dt.year
    df["month"] = df["ts"].dt.month
    df["day"] = df["ts"].dt.day
    df["dayofweek"] = df["ts"].dt.dayofweek
    return df


def train_and_evaluate(df, steps_ahead):
    """
    Trains a CatBoost model to predict the 'open' price and evaluates it on the test set,
    creating a rolling forecast and returning the plot as a matplotlib.pyplot figure.

    Parameters:
    df (pd.DataFrame): DataFrame containing the columns ['adjclose', 'close', 'high', 'low', 'open', 'ticker', 'ts', 'volume'].
    steps_ahead (int): The number of steps to forecast ahead.

    Returns:
    tuple: The trained model, the mean squared error on the test set, and the forecast plot as a matplotlib.pyplot figure.
    """
    # Check if necessary columns are in the DataFrame
    required_columns = {
        "adjclose",
        "close",
        "high",
        "low",
        "open",
        "ticker",
        "ts",
        "volume",
    }
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"DataFrame must contain the following columns: {required_columns}"
        )

    # Prepare data
    df["ts"] = pd.to_datetime(df["ts"])
    y = df["close"]
    X = df.drop(["adjclose", "close", "ticker"], axis=1)

    # Split into training and test sets
    train_size = int(len(X) * 0.9)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]
    X_train["ts"] = X_train["ts"].astype(int) / 10**9
    X_test["ts"] = X_test["ts"].astype(int) / 10**9
    # Train the model
    model = CatBoostRegressor(verbose=0)
    model.fit(X_train, y_train)

    # Rolling forecast
    predictions = []
    for i in range(len(X_test)):
        # Update the model to include the most recent observation in the training set
        model.fit(X.iloc[: train_size + i], y.iloc[: train_size + i], verbose=0)
        X_test_instance = X_test.iloc[i].to_frame().T
        X_test_instance["ts"] = (
            pd.to_datetime(X_test_instance["ts"]).astype(int) / 10**9
        )
        y_pred = model.predict(X_test_instance)
        predictions.append(y_pred[0])

    mse = mean_squared_error(y_test, predictions)

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(y_test.index, y_test, label="Actual")
    ax.plot(y_test.index, predictions, label="Forecast", alpha=0.7)
    ax.set_title("Rolling Forecast vs Actual")
    ax.set_xlabel("Index")
    ax.set_ylabel("Close Price")
    ax.legend()

    return model, mse, fig
