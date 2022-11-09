from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager
)
from typing import Any
from datetime import datetime



class EmptyStrategy(CtaTemplate):

    def __init__(self, cta_engine: Any, strategy_name: str, vt_symbol: str, setting: dict) -> None:
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.acc_delay = 0
        self.tick_count = 0
        self.display_tag = 10

    def on_tick(self, tick: TickData) -> None:
        # self.write_log(f"[stg on tick] {tick}")
        now = datetime.now()
        diff = now.timestamp() - tick.localtime.timestamp()
        # self.write_log(f"[now] {now} {now.timestamp()}")
        # self.write_log(f"[loc] {tick.localtime} {tick.localtime.timestamp()}")
        
        self.acc_delay += diff
        self.tick_count += 1
        if self.tick_count % self.display_tag == 0:
            self.write_log(f"mean delay of [{self.tick_count}]: {self.acc_delay / self.tick_count}")
        