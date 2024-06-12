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
    Trains a CatBoost model to predict the 'open' price and evaluates it once on the test set.

    Parameters:
    df (pd.DataFrame): DataFrame containing the columns ['adjclose', 'close', 'high', 'low', 'open', 'ticker', 'ts', 'volume'].
    test_size (float): The proportion of the dataset to include in the test split.

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
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=False
    )

    # Train the model
    model = CatBoostRegressor(verbose=0)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.plot(df["ts"], df["close"], label="Actual")
    plt.plot(X_test["ts"], y_pred, label="Predicted")
    plt.legend()
    plt.title("Prediction vs Actual")
    plt.xlabel("Time")
    plt.ylabel("Close Price")
    fig = plt.gcf()

    return model, mse, fig
