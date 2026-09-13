import pandas as pd
import yfinance as yf


def download_data(symbol, period, interval):
    """
    Download historical market data.

    This is intentionally kept outside the AI-modifiable
    strategy file.
    """

    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        raise RuntimeError(
            "No market data was returned."
        )

    # yfinance can sometimes return a MultiIndex.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    required = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise RuntimeError(
            f"Missing required columns: {missing}"
        )

    return df.dropna().copy()


def run_backtest(
    df,
    generate_signals,
    starting_capital=10000,
    transaction_cost=0.001
):
    """
    Very simple long-only backtester.

    This is NOT the final trading engine.

    Its purpose is to establish the automated
    research pipeline before we introduce VectorBT.
    """

    data = df.copy()

    signals = generate_signals(data)

    if not isinstance(signals, pd.Series):
        raise TypeError(
            "generate_signals(df) must return a pandas Series."
        )

    signals = signals.reindex(data.index)

    if signals.isna().all():
        raise ValueError(
            "Strategy produced no usable signals."
        )

    signals = signals.fillna(0).astype(int)

    # Ensure signals are only 0 or 1.
    invalid = ~signals.isin([0, 1])

    if invalid.any():
        raise ValueError(
            "Strategy signals must contain only 0 or 1."
        )

    # Shift positions by one bar to avoid using
    # today's closing information to trade at today's close.
    position = signals.shift(1).fillna(0)

    returns = data["Close"].pct_change().fillna(0)

    strategy_returns = position * returns

    # Transaction occurs when position changes.
    trades = position.diff().abs().fillna(0)

    strategy_returns -= (
        trades * transaction_cost
    )

    equity = (
        1 + strategy_returns
    ).cumprod() * starting_capital

    return {
        "equity": equity,
        "strategy_returns": strategy_returns,
        "position": position,
        "trades": trades
    }
