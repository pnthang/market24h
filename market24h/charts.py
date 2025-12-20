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
