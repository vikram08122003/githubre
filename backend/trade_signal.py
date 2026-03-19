import pandas as pd

df = pd.read_csv(
    r"C:\Users\vikra\OneDrive\Desktop\stock project\data\1  -NIFTY 50-05-06-2023-to-05-06-2024.csv"
)

# Clean column names
df.columns = df.columns.str.strip()

# Moving Averages
df['MA20'] = df['Close'].rolling(20).mean()
df['MA50'] = df['Close'].rolling(50).mean()

# RSI
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))

df = df.dropna()

# Signal logic
def signal(row):
    if row['RSI'] < 30 and row['MA20'] > row['MA50']:
        return "BUY"
    elif row['RSI'] > 70 and row['MA20'] < row['MA50']:
        return "SELL"
    else:
        return "HOLD"

df['Signal'] = df.apply(signal, axis=1)

print(df[['Date', 'Close', 'RSI', 'Signal']].tail())