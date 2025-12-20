

import streamlit as st

from market24h.data import fetch_data
from market24h.ui import show_price_chart, show_recent_data, show_company_info
from market24h.i18n import get_text
from market24h.technicals import add_technical_indicators
from market24h.charts import plot_advanced_chart


st.set_page_config(
    page_title="Market24h - AI Stock Dashboard",
    page_icon="📈",
    layout="wide"
)


# Language selection (default to Vietnamese)
lang = st.sidebar.selectbox(
    "🌐 Language / Ngôn ngữ",
    ["en", "vi"],
    index=1,  # 0 for English, 1 for Vietnamese
    format_func=lambda x: "English" if x=="en" else "Tiếng Việt"
)

st.title(get_text('title', lang))
st.markdown(get_text('subtitle', lang))



# Sidebar controls
st.sidebar.header(get_text('controls', lang))
symbol = st.sidebar.text_input(get_text('stock_symbol', lang), value="AAPL").upper()

# Time frame selection (like Yahoo Finance)
time_frames = {
    "1D": ("1d", "5m"),
    "5D": ("5d", "15m"),
    "1M": ("1mo", "30m"),
    "6M": ("6mo", "1d"),
    "YTD": ("ytd", "1d"),
    "1Y": ("1y", "1d"),
    "5Y": ("5y", "1d"),
    "All": ("max", "1d")
}
tf_label = st.sidebar.radio("Time Frame", list(time_frames.keys()), index=2)
period, interval = time_frames[tf_label]

data, info = fetch_data(symbol, period)
if interval != "1d":
    # For intraday, yfinance requires interval argument
    data, info = fetch_data(symbol, period)
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=interval)
    except Exception:
        pass

if data is None or data.empty:
    st.warning(get_text('no_data', lang))
    st.stop()




# Chart toggles
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Chart Options")
show_advanced = st.sidebar.checkbox("Show Advanced Technical Chart", value=True)
show_simple = st.sidebar.checkbox("Show Simple Price Chart", value=True)
show_table = st.sidebar.checkbox("Show Recent Data Table", value=True)
show_info = st.sidebar.checkbox("Show Company Info", value=True)

# Advanced chart component toggles
component_names = [
    ('Price', 'Price'),
    ('SMA_20', 'SMA 20'),
    ('SMA_50', 'SMA 50'),
    ('BB_Upper', 'BB Upper'),
    ('BB_Lower', 'BB Lower'),
    ('Volume', 'Volume'),
    ('MACD', 'MACD'),
    ('MACD_Signal', 'Signal'),
    ('RSI', 'RSI'),
    ('Stoch_K', 'Stoch %K'),
    ('Stoch_D', 'Stoch %D')
]
st.sidebar.markdown("**Advanced Chart Components**")
components = {}
for key, label in component_names:
    components[key] = st.sidebar.checkbox(label, value=True, key=f"comp_{key}")

# Add technical indicators
data_ta = add_technical_indicators(data)

if show_advanced:
    st.subheader("📈 Advanced Technical Analysis")
    st.plotly_chart(plot_advanced_chart(data_ta, symbol, components), use_container_width=True)
if show_simple:
    show_price_chart(symbol, data, lang)
if show_table:
    show_recent_data(data, lang)
if show_info and info:
    show_company_info(info, lang)
