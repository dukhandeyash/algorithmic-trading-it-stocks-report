import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def calculate_technical_indicators(df):

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift())
    low_close = abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    df['ATR'] = true_range.rolling(14).mean()

    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr14 = true_range.rolling(14).sum()
    plus_di14 = 100 * (plus_dm.rolling(14).sum() / tr14)
    minus_di14 = 100 * (minus_dm.rolling(14).sum() / tr14)
    df['ADX'] = (abs(plus_di14 - minus_di14) / (plus_di14 + minus_di14) * 100).rolling(14).mean()

    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()

    df['BB_middle'] = df['Close'].rolling(window=20).mean()
    df['BB_upper'] = df['BB_middle'] + 2 * df['Close'].rolling(window=20).std()
    df['BB_lower'] = df['BB_middle'] - 2 * df['Close'].rolling(window=20).std()

    return df

def plot_technical_analysis(df, symbol):
    fig = make_subplots(rows=4, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        row_heights=[0.4, 0.2, 0.2, 0.2])

    fig.add_trace(go.Candlestick(x=df.index,
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close'],
                                name='OHLC'), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], name='SMA20', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name='SMA50', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA200'], name='SMA200', line=dict(color='red')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper',
                            line=dict(color='gray', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower',
                            line=dict(color='gray', dash='dash')), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD',
                            line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['Signal_Line'], name='Signal Line',
                            line=dict(color='orange')), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                            line=dict(color='purple')), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['ADX'], name='ADX',
                            line=dict(color='brown')), row=4, col=1)
    fig.add_hline(y=25, line_dash="dash", line_color="gray", row=4, col=1)

    fig.update_layout(
        title=f'Technical Analysis for {symbol}',
        yaxis_title="Price",
        yaxis2_title="MACD",
        yaxis3_title="RSI",
        yaxis4_title="ADX",
        xaxis4_title="Date",
        height=1200,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    fig.show()

def analyze_stock(symbol, period='1y'):
    """
    Main function to perform technical analysis on a stock

    Parameters:
    symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT')
    period (str): Time period to analyze (e.g., '1y', '6mo', '3mo')
    """
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    df = calculate_technical_indicators(df)

    analysis = {
        'RSI_Status': 'Oversold' if df['RSI'].iloc[-1] < 30 else 'Overbought' if df['RSI'].iloc[-1] > 70 else 'Neutral',
        'MACD_Signal': 'Buy' if df['MACD'].iloc[-1] > df['Signal_Line'].iloc[-1] else 'Sell',
        'ADX_Trend_Strength': 'Strong' if df['ADX'].iloc[-1] > 25 else 'Weak',
        'SMA_Status': 'Bullish' if df['Close'].iloc[-1] > df['SMA200'].iloc[-1] else 'Bearish'
    }

    plot_technical_analysis(df, symbol)

    return analysis


if __name__ == "__main__":
    symbol = "Techm.ns"  
    analysis = analyze_stock(symbol, period='1y')
    print(f"\nTechnical Analysis Summary for {symbol}:")
    for key, value in analysis.items():
        print(f"{key}: {value}")