from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import yfinance as yf
import pandas as pd
import feedparser
from datetime import datetime
from analysis import predict_next_price

app = Flask(__name__)
app.secret_key = "stock_project_key"


def calculate_rsi(prices, period=14):
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)


def analyze_symbol(symbol):
    if not symbol.endswith(".NS"):
        symbol = symbol + ".NS"

    df = yf.download(symbol, period="2y", progress=False, auto_adjust=False)
    if df.empty:
        return None

    prices = df["Close"].values.flatten().tolist()
    dates  = [str(d.date()) for d in df.index]

    start_price   = round(prices[0], 2)
    current_price = round(prices[-1], 2)

    if prices[-1] > prices[0]:
        trend = "📈 Uptrend"
    elif prices[-1] < prices[0]:
        trend = "📉 Downtrend"
    else:
        trend = "➖ Sideways"

    rsi_series  = calculate_rsi(prices)
    rsi_values  = rsi_series.tolist()
    latest_rsi  = round(rsi_values[-1], 2)

    if latest_rsi < 30:
        signal = "BUY 🟢"
    elif latest_rsi > 70:
        signal = "SELL 🔴"
    else:
        signal = "HOLD 🟡"

    predicted_price      = predict_next_price(prices)
    price_change_percent = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)

    health_score = 50
    if latest_rsi < 30:
        health_score += 20
    elif latest_rsi > 70:
        health_score -= 20
    if trend == "📈 Uptrend":
        health_score += 15
    elif trend == "📉 Downtrend":
        health_score -= 15
    if predicted_price > current_price:
        health_score += 15
    else:
        health_score -= 10
    health_score = max(0, min(100, health_score))

    return dict(
        symbol=symbol,
        dates=dates,
        prices=prices,
        rsi_values=rsi_values,
        start_price=start_price,
        current_price=current_price,
        rsi=latest_rsi,
        signal=signal,
        trend=trend,
        predicted_price=predicted_price,
        price_change_percent=price_change_percent,
        health_score=health_score,
        current_time=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    symbol = request.form.get("symbol", "").upper().strip()
    result = analyze_symbol(symbol)
    if not result:
        return render_template("error.html", symbol=symbol)
    return render_template("result.html", **result)


@app.route("/news/<symbol>")
def news(symbol):
    clean = symbol.replace(".NS", "")
    url   = f"https://news.google.com/rss/search?q={clean}+stock+India&hl=en-IN&gl=IN&ceid=IN:en"
    feed  = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:6]:
        articles.append({
            "title":     entry.title,
            "link":      entry.link,
            "source":    entry.get("source", {}).get("title", "Google News"),
            "published": entry.get("published", "")
        })
    return jsonify(articles)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    s1 = request.values.get("s1", "").upper().strip()
    s2 = request.values.get("s2", "").upper().strip()

    if not s1 or not s2:
        return render_template("compare.html", data=None, s1=s1, s2=s2, compare_chart=None)

    d1 = analyze_symbol(s1)
    d2 = analyze_symbol(s2)

    if not d1 or not d2:
        return render_template("error.html", symbol=f"{s1} or {s2}")

    compare_chart = [
        {"symbol": d1["symbol"], "dates": d1["dates"], "prices": d1["prices"]},
        {"symbol": d2["symbol"], "dates": d2["dates"], "prices": d2["prices"]},
    ]

    return render_template(
        "compare.html",
        data=[d1, d2],
        s1=s1, s2=s2,
        compare_chart=compare_chart,
    )


@app.route("/add/<symbol>")
def add(symbol):
    session.setdefault("watchlist", [])
    if symbol not in session["watchlist"]:
        session["watchlist"].append(symbol)
    session.modified = True
    return redirect(url_for("watchlist"))


@app.route("/watchlist")
def watchlist():
    return render_template("watchlist.html", watchlist=session.get("watchlist", []))


@app.route("/remove/<symbol>")
def remove(symbol):
    if symbol in session.get("watchlist", []):
        session["watchlist"].remove(symbol)
        session.modified = True
    return redirect(url_for("watchlist"))


if __name__ == "__main__":
    app.run(debug=True)