import numpy as np
import pandas as pd
from xgboost import XGBRegressor

def predict_next_price(prices):

    if len(prices) < 30:
        return round(prices[-1], 2)

    df = pd.DataFrame(prices, columns=["Close"])

    # Feature engineering
    df["Lag1"]   = df["Close"].shift(1)
    df["Lag2"]   = df["Close"].shift(2)
    df["Lag3"]   = df["Close"].shift(3)
    df["MA5"]    = df["Close"].rolling(5).mean()
    df["MA10"]   = df["Close"].rolling(10).mean()
    df["MA20"]   = df["Close"].rolling(20).mean()
    df["Std5"]   = df["Close"].rolling(5).std()
    df["Return"] = df["Close"].pct_change()
    df["Next"]   = df["Close"].shift(-1)

    df.dropna(inplace=True)

    features = ["Lag1", "Lag2", "Lag3", "MA5", "MA10", "MA20", "Std5", "Return"]

    X = df[features]
    y = df["Next"]

    # Train XGBoost model
    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42,
        verbosity=0
    )

    model.fit(X, y)

    # Predict next price using latest available data
    last_row = X.iloc[-1].values.reshape(1, -1)
    prediction = model.predict(last_row)[0]

    return round(float(prediction), 2)
