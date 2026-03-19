import pandas as pd

# Load data
df = pd.read_csv(
    r"C:\Users\vikra\OneDrive\Desktop\stock project\data\1  -NIFTY 50-05-06-2023-to-05-06-2024.csv"
)

# REMOVE EXTRA SPACES IN COLUMN NAMES
df.columns = df.columns.str.strip()

# RSI calculation
delta = df['Close'].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()

rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))

df = df.dropna()

print(df[['Date', 'Close', 'RSI']].tail())
