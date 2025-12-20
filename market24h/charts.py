import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_advanced_chart(df, symbol, components=None):
    if components is None:
        components = {
            'Price': True,
            'SMA_20': True,
            'SMA_50': True,
            'BB_Upper': True,
            'BB_Lower': True,
            'Volume': True,
            'MACD': True,
            'MACD_Signal': True,
            'RSI': True,
            'Stoch_K': True,
            'Stoch_D': True
        }
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol} Price & MAs', 'Volume', 'MACD', 'RSI & Stochastic'),
        row_heights=[0.5, 0.15, 0.2, 0.15]
    )
    # Candlestick
    if components.get('Price'):
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
    # Moving averages
    if components.get('SMA_20'):
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='orange'), name='SMA 20'), row=1, col=1)
    if components.get('SMA_50'):
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='blue'), name='SMA 50'), row=1, col=1)
    # Bollinger Bands
    if components.get('BB_Upper'):
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='gray', width=1), name='BB Upper', showlegend=False), row=1, col=1)
    if components.get('BB_Lower'):
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='gray', width=1), name='BB Lower', fill='tonexty', fillcolor='rgba(128,128,128,0.1)', showlegend=False), row=1, col=1)
    # Volume
    if components.get('Volume'):
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color='lightblue', name='Volume'), row=2, col=1)
    # MACD
    if components.get('MACD'):
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='blue'), name='MACD'), row=3, col=1)
    if components.get('MACD_Signal'):
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], line=dict(color='orange'), name='Signal'), row=3, col=1)
    # RSI
    if components.get('RSI'):
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='purple'), name='RSI'), row=4, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=4, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=4, col=1)
    # Stochastic
    if components.get('Stoch_K'):
        fig.add_trace(go.Scatter(x=df.index, y=df['Stoch_K'], line=dict(color='gold'), name='Stoch %K'), row=4, col=1)
    if components.get('Stoch_D'):
        fig.add_trace(go.Scatter(x=df.index, y=df['Stoch_D'], line=dict(color='orange'), name='Stoch %D'), row=4, col=1)
    fig.update_layout(height=900, showlegend=True, template='plotly_white', font=dict(size=10))
    for i in range(1, 4):
        fig.update_xaxes(showticklabels=False, row=i, col=1)
    return fig
