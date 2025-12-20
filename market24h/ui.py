
import streamlit as st
import pandas as pd
from market24h.i18n import get_text

def show_price_chart(symbol, data, lang='en'):
    st.subheader(get_text('price_chart', lang, symbol=symbol))
    st.line_chart(data['Close'])

def show_recent_data(data, lang='en'):
    st.markdown(f"**{get_text('recent_data', lang)}**")
    data_show = data[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10)
    data_show.index = data_show.index.strftime('%Y-%m-%d')
    st.dataframe(data_show)

def show_company_info(info, lang='en'):
    st.sidebar.markdown("---")
    st.sidebar.write(f"**{get_text('company', lang)}:** {info.get('longName', 'N/A')}")
    st.sidebar.write(f"**{get_text('sector', lang)}:** {info.get('sector', 'N/A')}")
    st.sidebar.write(f"**{get_text('industry', lang)}:** {info.get('industry', 'N/A')}")
    st.sidebar.write(f"**{get_text('market_cap', lang)}:** {info.get('marketCap', 'N/A')}")
    st.sidebar.write(f"**{get_text('country', lang)}:** {info.get('country', 'N/A')}")
    st.sidebar.write(f"**{get_text('website', lang)}:** {info.get('website', 'N/A')}")
