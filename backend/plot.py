import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r"C:\Users\vikra\OneDrive\Desktop\stock project\data\1  -NIFTY 50-05-06-2023-to-05-06-2024.csv"
)

df.columns = df.columns.str.strip()

df['MA20'] = df['Close'].rolling(20).mean()
df['MA50'] = df['Close'].rolling(50).mean()

plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Close Price')
plt.plot(df['MA20'], label='MA20')
plt.plot(df['MA50'], label='MA50')
plt.legend()
plt.title("Stock Trend Analysis")
plt.show()
