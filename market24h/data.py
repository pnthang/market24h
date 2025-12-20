import yfinance as yf
import streamlit as st

def fetch_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        info = stock.info
        return data, info
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None
