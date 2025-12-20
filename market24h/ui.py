
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
    def _sanitize(val):
        if val is None:
            return 'N/A'
        if not isinstance(val, str):
            val = str(val)
        # Escape dollar signs to avoid Streamlit math parsing on some devices
        return val.replace('$', '\\$')

    st.markdown("---")
    st.write(f"**{get_text('company', lang)}:** {_sanitize(info.get('longName'))}")
    st.write(f"**{get_text('sector', lang)}:** {_sanitize(info.get('sector'))}")
    st.write(f"**{get_text('industry', lang)}:** {_sanitize(info.get('industry'))}")
    st.write(f"**{get_text('market_cap', lang)}:** {_sanitize(info.get('marketCap'))}")
    st.write(f"**{get_text('country', lang)}:** {_sanitize(info.get('country'))}")
    st.write(f"**{get_text('website', lang)}:** {_sanitize(info.get('website'))}")
