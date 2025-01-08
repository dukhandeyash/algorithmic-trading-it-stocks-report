# Algorithmic Trading Report on IT Sector Stocks

This project provides a comprehensive study of the IT sector, focusing on the fundamental and technical analysis of major IT sector stocks. It utilizes various Python libraries for data collection, analysis, and visualization, along with technical indicators such as RSI, MACD, ADX, and moving averages to analyze stock trends and generate trading signals.

## Table of Contents
1. [Introduction](#introduction)
2. [Overview of IT Sector](#overview-of-it-sector)
3. [Understanding Fundamental and Technical Analysis](#understanding-fundamental-and-technical-analysis)
4. [Stock Analysis (Fundamental Analysis)](#stock-analysis-fundamental-analysis)
5. [Stock Analysis (Technical Analysis)](#stock-analysis-technical-analysis)
6. [Final Verdict](#final-verdict)

## Project Overview
This report focuses on analyzing stocks in the IT sector using both fundamental and technical analysis. The technical analysis is implemented with the help of Python, utilizing popular libraries like `pandas`, `numpy`, `yfinance`, and `plotly` for stock data retrieval, indicator calculation, and plotting.

## Key Features:
- **Technical Indicators**: The following technical indicators are calculated:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - ADX (Average Directional Index)
  - Simple Moving Averages (SMA) for 20, 50, and 200 days
  - Bollinger Bands (upper and lower)
  
- **Stock Data**: Data for IT sector stocks is retrieved using `yfinance`, including historical data for a specified time period.

- **Technical Analysis Plot**: The report generates a plot with multiple subplots, showing:
  - Candlestick chart with SMA and Bollinger Bands
  - MACD and its Signal Line
  - RSI with overbought/oversold lines
  - ADX with trend strength indication

## Requirements:
- Python 3.x
- `pandas` library
- `numpy` library
- `yfinance` library
- `plotly` library

You can install the required libraries using pip:

```bash
pip install pandas numpy yfinance plotly
