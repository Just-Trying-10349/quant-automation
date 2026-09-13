import pandas as pd


def generate_signals(df):
    """
    Simple baseline strategy.

    BUY/long signal:
        EMA 20 > EMA 50

    No position:
        EMA 20 <= EMA 50

    This is intentionally simple.
    The purpose of the first stage is to prove that:

        GitHub
        ↓
        strategy
        ↓
        backtester
        ↓
        AI
        ↓
        modified strategy
        ↓
        evaluation

    all work correctly.
    """

    data = df.copy()

    # Calculate the two moving averages.
    data["ema_20"] = data["Close"].ewm(
        span=20,
        adjust=False
    ).mean()

    data["ema_50"] = data["Close"].ewm(
        span=50,
        adjust=False
    ).mean()

    # Generate a binary position signal.
    data["signal"] = (
        data["ema_20"] > data["ema_50"]
    ).astype(int)

    return data["signal"]
