

import streamlit as st
from market24h.data import fetch_data
from market24h.ui import show_price_chart, show_recent_data, show_company_info
from market24h.i18n import get_text


st.set_page_config(
    page_title="Market24h - AI Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# Language selection
lang = st.sidebar.selectbox("🌐 Language / Ngôn ngữ", ["en", "vi"], format_func=lambda x: "English" if x=="en" else "Tiếng Việt")

st.title(get_text('title', lang))
st.markdown(get_text('subtitle', lang))

st.dataframe(data_show)

# Sidebar controls
st.sidebar.header(get_text('controls', lang))
symbol = st.sidebar.text_input(get_text('stock_symbol', lang), value="AAPL").upper()
period = st.sidebar.selectbox(get_text('period', lang), ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

data, info = fetch_data(symbol, period)

if data is None or data.empty:
    st.warning(get_text('no_data', lang))
    st.stop()

show_price_chart(symbol, data, lang)
show_recent_data(data, lang)
if info:
    show_company_info(info, lang)
