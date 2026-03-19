import yfinance as yf

# NIFTY 50 index
ticker = yf.Ticker("^NSEI")

df = ticker.history(period="6mo")

print(df.head())
