import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

class StockAPI:

    def __init__(self):
        self.api_key = st.secrets["API_KEY"]
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }

    def symbol_search(self, company: str):
        querystring = {
            "datatype": "json",
            "keywords": company,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        d = {}
        for i in data["bestMatches"]:
            symbol = i["1. symbol"]
            d[symbol] = [i["2. name"], i["4. region"], i["8. currency"]]

        return d

    def get_daily_prices(self, symbol: str):
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        daily = data["Time Series (Daily)"]
        df = pd.DataFrame(daily).T
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"
        df = df.astype(float)
        return df

    def plot_candlestick(self, df: pd.DataFrame):
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df["1. open"],
                    high=df["2. high"],
                    low=df["3. low"],
                    close=df["4. close"],
                )
            ]
        )

        fig.update_layout(width=1200, height=800)

        return fig