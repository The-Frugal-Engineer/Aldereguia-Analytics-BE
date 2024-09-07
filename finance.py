import yfinance as yf
import pandas as pd

from files import write_panda_to_file

all_tickers = {
    "^GSPC": {"description": "S&P 500 Index", "type": "Index"},
    "^DJI": {"description": "Dow Jones Industrial Average", "type": "Index"},
    "^IXIC": {"description": "Nasdaq Composite Index", "type": "Index"},
    "^RUT": {"description": "Russell 2000 Index", "type": "Index"},
    "^FTSE": {"description": "FTSE 100 Index", "type": "Index"},
    "^N225": {"description": "Nikkei 225 Index", "type": "Index"},
    "SPY": {"description": "SPDR S&P 500 ETF Trust", "type": "ETF"},
    "QQQ": {"description": "Invesco QQQ Trust", "type": "ETF"},
    "VTI": {"description": "Vanguard Total Stock Market ETF", "type": "ETF"},
    "EEM": {"description": "iShares MSCI Emerging Markets ETF", "type": "ETF"},
    "IWM": {"description": "iShares Russell 2000 ETF", "type": "ETF"},
    "URTH": {"description": "iShares MSCI World ETF", "type": "ETF"},
    "AAPL": {"description": "Apple Inc.", "type": "Stock"},
    "MSFT": {"description": "Microsoft Corporation", "type": "Stock"},
    "AMZN": {"description": "Amazon.com, Inc.", "type": "Stock"},
    "GOOGL": {"description": "Alphabet Inc.", "type": "Stock"},
    "META": {"description": "Meta Platforms, Inc.", "type": "Stock"},
    "TSLA": {"description": "Tesla, Inc.", "type": "Stock"},
    "BRK-B": {"description": "Berkshire Hathaway Inc.", "type": "Stock"},
    "JNJ": {"description": "Johnson & Johnson", "type": "Stock"},
    "JPM": {"description": "JPMorgan Chase & Co.", "type": "Stock"},
    "NVDA": {"description": "NVIDIA Corporation", "type": "Stock"},
    "GC=F": {"description": "Gold Futures", "type": "Commodity"},
    "SI=F": {"description": "Silver Futures", "type": "Commodity"},
    "CL=F": {"description": "Crude Oil (WTI) Futures", "type": "Commodity"},
    "NG=F": {"description": "Natural Gas Futures", "type": "Commodity"},
    "EURUSD=X": {"description": "Euro to US Dollar", "type": "Currency"},
    "GBPUSD=X": {"description": "British Pound to US Dollar", "type": "Currency"},
    "JPY=X": {"description": "US Dollar to Japanese Yen", "type": "Currency"},
    "BTC-USD": {"description": "Bitcoin to US Dollar", "type": "Cryptocurrency"},
    "^TNX": {"description": "US 10-Year Treasury Yield", "type": "Bond"},
    "^TYX": {"description": "US 30-Year Treasury Yield", "type": "Bond"}
}

default_start_date="2004-01-01"
default_end_date="2024-08-01"

def refresh_asset(asset, start_date, end_date, resample='ME'):
    asset = yf.download(asset, start=start_date, end=end_date)

    return asset


def refresh_all_assets():
    for ticker, info in all_tickers.items():
        description = info['description']
        type_ = info['type']
        print(f"Ticker: {ticker}, Description: {description}, Type: {type_}")
        asset_matrix=refresh_asset(ticker, default_start_date, default_end_date)
        write_panda_to_file(asset_matrix, ticker)

