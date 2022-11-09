from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy_ctastrategy.strategies.atr_rsi_strategy import (
    AtrRsiStrategy,
)
from datetime import datetime
import pandas as pd
import pprint


def show_order(df: pd.DataFrame):
    trade_list = []
    for trades in df.pop("trades"):
        for trade in trades:
            trade_list.append(trade)
    
    trade_df = pd.DataFrame(trade_list)
    print("orders", "-" * 60)
    print(df)
    print("trades", "-" * 60)
    print(trade_df)


def run():

    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol="600000.SSE",
        interval="d",
        start=datetime(2012, 1, 1),
        end=datetime(2022, 11, 4),
        rate=0.3/10000,
        slippage=0.2,
        size=300,
        pricetick=0.2,
        capital=1_000_000,
    )
    engine.add_strategy(AtrRsiStrategy, {})

    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    stat = engine.calculate_statistics()
    show_order(df)
    pprint.pprint(stat)
    # engine.show_chart()

if __name__ == "__main__":
    run()