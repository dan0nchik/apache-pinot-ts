from datetime import datetime
import json
import time
import streamlit as st
from connection import fetch_places_data, fetch_news
import plotly.graph_objects as go
import plotly.express as px


# main page
def main():
    st.title("Software system for assessing the impact of news on stock prices")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Stocks", "News"])

    if page == "News":
        news_page()
    elif page == "Stocks":
        stocks_page()


# new
def news_page():
    st.title("News")
    fetch_button = st.button("Fetch News")
    if fetch_button:
        df = fetch_news()
        for index, row in df.iterrows():
            st.json(row["entry_json"])


# stocks
def stocks_page():
    with open("config.json") as f:
        config = json.load(f)
    col1, col2 = st.columns(2)
    with col1:
        st.title("Stocks")
        stock_providers = config["providers"].keys()
        selected_provider = st.selectbox("Select a provider", stock_providers)
        stocks_options = config["providers"][selected_provider]["tickers"]
        columns = config["providers"][selected_provider]["columns"]
        selected_stock = st.selectbox("Select a stock option", stocks_options)
        n = st.number_input("Last N values", min_value=1, max_value=10000, value=100)
    with col2:
        stock_page(selected_stock, columns, selected_provider, n)


def stock_page(stock_name, columns, provider, n):
    line_chart = st.empty()
    candle_chart = st.empty()
    while True:
        df = fetch_places_data(stock_name, columns)[-n:]
        # line_chart.empty()
        with line_chart.container():
            if provider == "yahoo":
                fig = px.line(df, x="ts", y="price")
                fig.update_yaxes(domain=(0.25, 0.75))
                st.plotly_chart(fig, use_container_width=True)
            if provider == "tinkoff":
                fig = px.line(df, x="ts", y="open")
                fig.update_yaxes(domain=(0.25, 0.75))
                st.plotly_chart(fig, use_container_width=True)
        if provider == "tinkoff":
            # df["ts"] = df["ts"].apply(lambda x: datetime.fromtimestamp(x / 1e3))
            # candle_chart.empty()
            with candle_chart.container():
                fig = go.Figure(
                    data=[
                        go.Candlestick(
                            x=df["ts"],
                            open=df["open"],
                            high=df["high"],
                            low=df["low"],
                            close=df["close"],
                        )
                    ]
                )
                fig.update_layout(xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
        if provider == "yahoo":
            candle_chart.empty()


if __name__ == "__main__":
    main()
