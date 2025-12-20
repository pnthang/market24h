from market24h.db import save_dataframe


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
lang = st.selectbox(
    "🌐 Language / Ngôn ngữ",
    ["en", "vi"],
    index=1,
    format_func=lambda x: "English" if x=="en" else "Tiếng Việt"
)

st.title(get_text('title', lang))

# Mobile-first: vertical stacking for controls
st.markdown(get_text('subtitle', lang))
top_stocks = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "NVIDIA (NVDA)": "NVDA",
    "Meta (META)": "META",
    "Tesla (TSLA)": "TSLA",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "Visa (V)": "V",
    "JPMorgan Chase (JPM)": "JPM",
    "Johnson & Johnson (JNJ)": "JNJ",
    "UnitedHealth (UNH)": "UNH",
    "Eli Lilly (LLY)": "LLY",
    "Walmart (WMT)": "WMT",
    "Mastercard (MA)": "MA",
    "Procter & Gamble (PG)": "PG",
    "Broadcom (AVGO)": "AVGO",
    "Home Depot (HD)": "HD",
    "Exxon Mobil (XOM)": "XOM",
    "Coca-Cola (KO)": "KO"
}
st.markdown("---")
st.markdown("### Select Stock")
stock_choice = st.selectbox("Select Stock", list(top_stocks.keys()) + ["Custom"], index=0)
if stock_choice == "Custom":
    symbol = st.text_input(get_text('stock_symbol', lang), value="AAPL").upper()
else:
    symbol = top_stocks[stock_choice]

# Time frame selection (like Yahoo Finance)

# Move Time Frame selection below Advanced Chart Components
st.markdown("---")
st.markdown("**Time Frame**")
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
tf_selected = st.pills(
    "Time Frame",
    options=list(time_frames.keys()),
    selection_mode="single",
    default=[list(time_frames.keys())[2]],
    key="timeframe_pills"
)
tf_label = tf_selected[0] if tf_selected else list(time_frames.keys())[2]
tf_label_clean = tf_label.strip() if isinstance(tf_label, str) else list(time_frames.keys())[2]
if tf_label_clean not in time_frames:
    tf_label_clean = list(time_frames.keys())[2]
period, interval = time_frames[tf_label_clean]

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

# Move chart options to top of main content area


st.markdown("---")
st.subheader("📊 Chart Options")
chart_options = [
    "Show Advanced Technical Chart",
    "Show Simple Price Chart",
    "Show Recent Data Table",
    "Show Company Info"
]
selected_chart_options = st.pills(
    "Chart Options",
    options=chart_options,
    selection_mode="multi",
    default=chart_options,
    key="chart_options_pills"
)
show_advanced = "Show Advanced Technical Chart" in selected_chart_options
show_simple = "Show Simple Price Chart" in selected_chart_options
show_table = "Show Recent Data Table" in selected_chart_options
show_info = "Show Company Info" in selected_chart_options

# Advanced chart component toggles (below chart options)
st.markdown("**Advanced Chart Components**")
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
component_labels = [label for key, label in component_names]
selected_components = st.pills(
    "Advanced Chart Components",
    options=component_labels,
    selection_mode="multi",
    default=component_labels,
    key="components_pills"
)
components = {key: (label in selected_components) for key, label in component_names}

# Add technical indicators
data_ta = add_technical_indicators(data)

if show_advanced:
    st.subheader("📈 Advanced Technical Analysis")
    show_price_chart(symbol, data, lang)
    st.plotly_chart(plot_advanced_chart(data_ta, symbol, components), use_container_width=True)
if show_simple:
    # Price chart is now merged into Advanced Technical Analysis
    pass
if show_table:
    show_recent_data(data, lang)
    if st.button(f"Save {symbol} Data to PostgreSQL"):
        save_dataframe(data.reset_index(), f"{symbol.lower()}_stock_data")
        st.success(f"{symbol} data saved to PostgreSQL!")
if show_info and info:
    show_company_info(info, lang)
print(tf_label, time_frames.keys())
