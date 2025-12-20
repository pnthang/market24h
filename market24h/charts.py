import plotly.graph_objects as go


def plot_advanced_chart(df, symbol, components=None):
    """Render all selected components on a single chart with volume on a secondary y-axis."""
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

    fig = go.Figure()

    # Price (candlestick)
    if components.get('Price') and {'Open', 'High', 'Low', 'Close'}.issubset(df.columns):
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ))

    # Moving averages and bands
    if components.get('SMA_20') and 'SMA_20' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20'))
    if components.get('SMA_50') and 'SMA_50' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50'))
    if components.get('BB_Upper') and 'BB_Upper' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], mode='lines', name='BB Upper', line=dict(width=1), showlegend=False))
    if components.get('BB_Lower') and 'BB_Lower' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], mode='lines', name='BB Lower', fill='tonexty', fillcolor='rgba(128,128,128,0.1)', showlegend=False))

    # Volume (secondary y-axis)
    if components.get('Volume') and 'Volume' in df:
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue', opacity=0.3, yaxis='y2'))

    # Technical indicators as overlays
    if components.get('MACD') and 'MACD' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD'))
    if components.get('MACD_Signal') and 'MACD_Signal' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name='MACD Signal'))
    if components.get('RSI') and 'RSI' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'))
    if components.get('Stoch_K') and 'Stoch_K' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['Stoch_K'], mode='lines', name='Stoch %K'))
    if components.get('Stoch_D') and 'Stoch_D' in df:
        fig.add_trace(go.Scatter(x=df.index, y=df['Stoch_D'], mode='lines', name='Stoch %D'))

    # Layout: primary y for price/indicators, secondary y for volume
    fig.update_layout(
        title=f"{symbol} - Complete Technical Analysis",
        xaxis=dict(type='date', showspikes=True, spikemode='across', spikesnap='cursor'),
        yaxis=dict(title='Price'),
        yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False),
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )

    return fig


def create_performance_metrics(data, symbol):
    """Create performance metrics visualization (returns, volatility, sharpe, drawdown)."""
    import numpy as np
    data = data.copy()
    data['Daily_Returns'] = data['Close'].pct_change()
    data['Cumulative_Returns'] = (1 + data['Daily_Returns']).cumprod() - 1
    total_return = data['Cumulative_Returns'].iloc[-1] * 100
    volatility = data['Daily_Returns'].std() * np.sqrt(252) * 100 if data['Daily_Returns'].std() is not None else 0
    sharpe_ratio = (data['Daily_Returns'].mean() * 252) / (data['Daily_Returns'].std() * np.sqrt(252)) if data['Daily_Returns'].std() not in (0, None) else 0
    max_drawdown = ((data['Close'] / data['Close'].expanding().max()) - 1).min() * 100

    # Metrics as a small dict for display
    metrics = {
        'total_return': total_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }

    # cumulative returns chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Returns'] * 100, mode='lines', name='Cumulative Returns', line=dict(color='#00ff88', width=2)))
    fig.update_layout(title=f'{symbol} Cumulative Returns (%)', xaxis_title='Date', yaxis_title='Cumulative Return (%)', template='plotly_dark', height=360)

    return metrics, fig


def create_advanced_chart(data, symbol):
    """Create advanced chart using subplots:
    Row1: Candles + MAs + Bollinger (Bollinger drawn behind candles)
    Row2: Volume (+ Vol SMA)
    Row3: MACD (lines + histogram)
    Row4: RSI + Stochastic (+ reference lines)
    """
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_heights=[0.5, 0.15, 0.2, 0.15],
                        subplot_titles=(f'{symbol} Price Action & Moving Averages', 'Volume', 'MACD', 'RSI & Stochastic'))

    # Determine Bollinger column names
    bb_upper_col = None
    bb_lower_col = None
    if 'BB_upper' in data.columns and 'BB_lower' in data.columns:
        bb_upper_col, bb_lower_col = 'BB_upper', 'BB_lower'
    elif 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
        bb_upper_col, bb_lower_col = 'BB_Upper', 'BB_Lower'

    # Moving averages (draw before candles)
    mas = [('SMA_20', 'SMA 20'), ('SMA_50', 'SMA 50'), ('SMA_200', 'SMA 200')]
    ma_colors = ['#ff7f0e', '#1f77b4', '#9467bd']
    for i, (col, label) in enumerate(mas):
        if col in data.columns and not data[col].isna().all():
            fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=label, line=dict(color=ma_colors[i], width=1.8)), row=1, col=1)

    # Bollinger Bands first so fill is behind candles (low opacity)
    if bb_upper_col and bb_lower_col:
        fig.add_trace(go.Scatter(x=data.index, y=data[bb_upper_col], mode='lines', line=dict(width=0), name='BB Upper', showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data[bb_lower_col], mode='lines', line=dict(width=0), name='BB Lower', fill='tonexty', fillcolor='rgba(120,120,120,0.12)', showlegend=False), row=1, col=1)

    # Candles (draw after bands so they appear on top)
    if {'Open', 'High', 'Low', 'Close'}.issubset(data.columns):
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                                     name='Price', increasing_line_color='#2ca02c', decreasing_line_color='#d62728', showlegend=True, opacity=1.0), row=1, col=1)

    # Volume row
    if 'Volume' in data.columns:
        vol_colors = ['#2ca02c' if (row['Close'] >= row['Open']) else '#d62728' for _, row in data[['Open','Close']].iterrows()]
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color=vol_colors, name='Volume', opacity=0.85, showlegend=True), row=2, col=1)
        if 'Volume_SMA' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['Volume_SMA'], mode='lines', name='Vol SMA', line=dict(color='#1f77b4', width=1.2)), row=2, col=1)

    # MACD row
    if 'MACD' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD', line=dict(color='#1f77b4', width=1.5)), row=3, col=1)
    sig_col = 'MACD_signal' if 'MACD_signal' in data.columns else ('MACD_Signal' if 'MACD_Signal' in data.columns else None)
    if sig_col:
        fig.add_trace(go.Scatter(x=data.index, y=data[sig_col], mode='lines', name='Signal', line=dict(color='#ff7f0e', width=1.5)), row=3, col=1)
    if 'MACD_histogram' in data.columns:
        hist = data['MACD_histogram']
        hist_colors = ['#2ca02c' if v >= 0 else '#d62728' for v in hist]
        fig.add_trace(go.Bar(x=data.index, y=hist, marker_color=hist_colors, name='Histogram', opacity=0.8), row=3, col=1)

    # RSI & Stochastic row
    if 'RSI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', line=dict(color='#9467bd', width=1.5)), row=4, col=1)
        fig.add_hline(y=70, line_dash='dash', line_color='red', opacity=0.7, row=4, col=1)
        fig.add_hline(y=30, line_dash='dash', line_color='green', opacity=0.7, row=4, col=1)
        fig.add_hline(y=50, line_dash='dot', line_color='gray', opacity=0.5, row=4, col=1)
    if 'Stoch_K' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['Stoch_K'], mode='lines', name='Stoch %K', line=dict(color='#ffcc00', width=1.2)), row=4, col=1)
    if 'Stoch_D' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['Stoch_D'], mode='lines', name='Stoch %D', line=dict(color='#ff6600', width=1.2)), row=4, col=1)

    # Layout & styling to match mockup
    fig.update_layout(title=f'{symbol} Price Action & Moving Averages', xaxis_rangeslider_visible=False, height=760,
                      showlegend=True, template='plotly_white', font=dict(size=11),
                      legend=dict(orientation='v', y=0.98, x=1.02, bordercolor='#ddd', borderwidth=0),
                      margin=dict(l=60, r=220, t=60, b=40))

    # hide x tick labels for upper subplots
    for r in (1, 2, 3):
        fig.update_xaxes(showticklabels=False, row=r, col=1)

    # RSI axis range
    if 'RSI' in data.columns:
        fig.update_yaxes(range=[0, 100], row=4, col=1)

    # axis titles
    fig.update_yaxes(title_text='Price', row=1, col=1)
    fig.update_yaxes(title_text='Volume', row=2, col=1)
    fig.update_yaxes(title_text='MACD', row=3, col=1)
    fig.update_yaxes(title_text='RSI / Stoch', row=4, col=1)

    return fig
