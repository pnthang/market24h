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
    """Create an advanced candlestick chart with technical indicators overlaid and
    volume shown on a secondary y-axis."""
    fig = go.Figure()

    # Candlestick
    if {'Open', 'High', 'Low', 'Close'}.issubset(data.columns):
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price',
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff4444'
        ))

    # Moving averages
    mas = [('SMA_20', 'SMA 20'), ('SMA_50', 'SMA 50'), ('SMA_200', 'SMA 200')]
    colors = ['#ff9500', '#007aff', '#5856d6']
    for i, (col, label) in enumerate(mas):
        if col in data.columns and not data[col].isna().all():
            fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=label, line=dict(color=colors[i], width=1.5)))

    # Bollinger Bands
    if 'BB_upper' in data.columns and 'BB_lower' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], mode='lines', line=dict(color='rgba(200,200,200,0.5)', width=1), name='BB Upper', showlegend=False))
        fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], mode='lines', line=dict(color='rgba(200,200,200,0.5)', width=1), name='BB Lower', fill='tonexty', fillcolor='rgba(200,200,200,0.08)', showlegend=False))

    # Volume on secondary axis
    if 'Volume' in data.columns:
        vol_colors = ['#00ff88' if row['Close'] >= row['Open'] else '#ff4444' for _, row in data[['Open', 'Close']].iterrows()]
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=vol_colors, opacity=0.6, yaxis='y2'))

    # MACD
    if 'MACD' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD', line=dict(color='#007aff', width=1.5)))
    sig_col = 'MACD_signal' if 'MACD_signal' in data.columns else ('MACD_Signal' if 'MACD_Signal' in data.columns else None)
    if sig_col:
        fig.add_trace(go.Scatter(x=data.index, y=data[sig_col], mode='lines', name='Signal', line=dict(color='#ff9500', width=1.5)))
    if 'MACD_histogram' in data.columns:
        hist = data['MACD_histogram']
        hist_colors = ['#00ff88' if v >= 0 else '#ff4444' for v in hist]
        fig.add_trace(go.Bar(x=data.index, y=hist, name='MACD Histogram', marker_color=hist_colors, opacity=0.5))

    # RSI
    if 'RSI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', line=dict(color='#af52de', width=1.5)))
        fig.add_hline(y=70, line_dash='dash', line_color='red', opacity=0.6)
        fig.add_hline(y=30, line_dash='dash', line_color='green', opacity=0.6)

    # Stochastic
    if 'Stoch_K' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['Stoch_K'], mode='lines', name='Stoch %K', line=dict(color='#ffcc00', width=1)))
    if 'Stoch_D' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['Stoch_D'], mode='lines', name='Stoch %D', line=dict(color='#ff6600', width=1)))

    fig.update_layout(
        title=f'{symbol} - Advanced Technical Chart',
        template='plotly_dark',
        xaxis=dict(rangeslider=dict(visible=False)),
        yaxis=dict(title='Price'),
        yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False, position=1.0),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified',
        height=800
    )

    return fig
