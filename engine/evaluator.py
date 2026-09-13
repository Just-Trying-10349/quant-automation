import math


def calculate_metrics(backtest):
    """
    Convert raw backtest results into measurable metrics.
    """

    equity = backtest["equity"]
    returns = backtest["strategy_returns"]
    trades = backtest["trades"]

    starting_value = float(equity.iloc[0])
    ending_value = float(equity.iloc[-1])

    total_return = (
        ending_value / starting_value
    ) - 1

    # Maximum drawdown.
    running_max = equity.cummax()

    drawdown = (
        equity / running_max
    ) - 1

    max_drawdown = abs(float(drawdown.min()))

    # Approximate annualized Sharpe.
    if returns.std() == 0:
        sharpe = 0.0
    else:
        sharpe = (
            returns.mean()
            / returns.std()
        ) * math.sqrt(365)

    trade_count = int(
        trades.sum() / 2
    )

    win_rate = float(
        (returns > 0).mean()
    )

    return {
        "total_return": round(total_return, 6),
        "sharpe": round(float(sharpe), 6),
        "max_drawdown": round(max_drawdown, 6),
        "trade_count": trade_count,
        "win_rate": round(win_rate, 6),
        "ending_equity": round(ending_value, 2)
    }


def calculate_score(metrics):
    """
    Deterministic evaluation.

    The AI does NOT decide whether it won.

    GitHub calculates the score.
    """

    return (
        metrics["sharpe"]
        + metrics["total_return"] * 2
        - metrics["max_drawdown"] * 2
    )


def is_better(candidate, current_best):
    """
    Decide whether the candidate is objectively better.
    """

    if current_best is None:
        return True

    return candidate["score"] > current_best["score"]
