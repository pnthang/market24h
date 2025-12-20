LANGUAGES = {
    'en': {
        'title': "Market24h - AI Stock Dashboard",
        'subtitle': "*AI-powered technical analysis and predictions*",
        'controls': "Controls",
        'stock_symbol': "Stock Symbol",
        'period': "Period",
        'price_chart': "{symbol} Price Chart",
        'recent_data': "Recent Data",
        'company': "Company",
        'sector': "Sector",
        'industry': "Industry",
        'market_cap': "Market Cap",
        'country': "Country",
        'website': "Website",
        'no_data': "No data found. Check the symbol and try again."
    },
    'vi': {
        'title': "Market24h",
        'subtitle': "*Phân tích kỹ thuật và dự đoán bằng AI*",
        'controls': "Điều khiển",
        'stock_symbol': "Mã cổ phiếu",
        'period': "Khoảng thời gian",
        'price_chart': "Biểu đồ giá {symbol}",
        'recent_data': "Dữ liệu gần đây",
        'company': "Công ty",
        'sector': "Ngành",
        'industry': "Lĩnh vực",
        'market_cap': "Vốn hóa thị trường",
        'country': "Quốc gia",
        'website': "Website",
        'no_data': "Không tìm thấy dữ liệu. Kiểm tra lại mã cổ phiếu."
    }
}

def get_text(key, lang='en', **kwargs):
    text = LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
