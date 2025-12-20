

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
period = st.sidebar.selectbox(get_text('period', lang), ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

data, info = fetch_data(symbol, period)

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

# Add technical indicators
data_ta = add_technical_indicators(data)

if show_advanced:
    st.subheader("📈 Advanced Technical Analysis")
    st.plotly_chart(plot_advanced_chart(data_ta, symbol), use_container_width=True)
if show_simple:
    show_price_chart(symbol, data, lang)
if show_table:
    show_recent_data(data, lang)
if show_info and info:
    show_company_info(info, lang)
