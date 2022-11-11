# 回测

## 安装模块

```txt
vnpy_ctastrategy
vnpy_datamanager
vnpy_tushare
vnpy_sqlite
```

## 下载历史数据

下载历史数据需要用到以下模块：

* vnpy_datamanager: 历史数据管理模块，负责历史数据下载，整理，读取和回放等操作
  * datafeed: 数据服务适配器接口，用于从数据源获取历史数据，这里使用`vnpy_tushare`的实现。
  * database: 数据库接口，用于在本地环境读写历史数据，这里使用`vnpy_sqlite`的实现。

### `tushare`使用

`tushare`目前需要注册账号，在调用接口的时候需要添加token作为参数才能正常获取数据。

* `tushare`注册: https://tushare.pro/
* `tushare`个人主页查看`$TOKEN`: https://tushare.pro/user/token
* `tushare`更新个人信息（获取数据有权限限制，需要一定的积分，更新完个人信息后可以下载日频数据): https://tushare.pro/user/info。

### 历史数据更新代码案例

```python
from vnpy.trader import setting
from vnpy_datamanager.engine import ManagerEngine, MainEngine
from vnpy.trader.constant import Exchange
from datetime import datetime


# 设置datafeed为tushare
setting.SETTINGS["datafeed.name"] = "tushare"
# tushare账号
setting.SETTINGS["datafeed.username"] = ""
# tushare $TOKEN
setting.SETTINGS["datafeed.password"] = "$TOKEN"

# 设置datafeed为sqlite
setting.SETTINGS["database.name"] = "sqlite"
setting.SETTINGS["database.database"] = "database.db"


def download(manager: ManagerEngine):

    result = manager.download_bar_data(
        symbol="600000",
        exchange=Exchange.SSE,
        interval="d",
        start=datetime(2012, 1, 1)
    )

    print("download result", result)


def main():
    me = MainEngine()
    
    manager = ManagerEngine(me, me.event_engine)
    
    try:
        download(manager)
    
    finally:
        
        manager.event_engine.stop()
        manager.main_engine.close()


if __name__ == "__main__":
    main()

```

## Backtest

回测使用vnpy_ctastrategy的回测引擎

```python
from vnpy_ctastrategy.backtesting import BacktestingEngine
# 使用样本策略
from vnpy_ctastrategy.strategies.atr_rsi_strategy import (
    AtrRsiStrategy,
)
from datetime import datetime
import pandas as pd
import pprint


# 使用sqlite作为数据库
setting.SETTINGS["database.name"] = "sqlite"


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
```

输出

```
2022-11-04 14:10:08.925097      开始加载历史数据
2022-11-04 14:10:08.925097      加载进度：# [0%]
2022-11-04 14:10:08.961000      加载进度：## [10%]
2022-11-04 14:10:08.975961      加载进度：### [20%]
2022-11-04 14:10:08.990950      加载进度：#### [30%]
2022-11-04 14:10:09.004913      加载进度：##### [40%]
2022-11-04 14:10:09.019845      加载进度：###### [50%]
2022-11-04 14:10:09.036800      加载进度：####### [60%]
2022-11-04 14:10:09.050201      加载进度：######## [70%]
2022-11-04 14:10:09.065163      加载进度：######### [80%]
2022-11-04 14:10:09.078132      加载进度：########## [90%]
2022-11-04 14:10:09.097052      历史数据加载完成，数据量：2598
2022-11-04 14:10:09.097052      策略初始化完成
2022-11-04 14:10:09.097052      开始回放历史数据
2022-11-04 14:10:09.107055      回放进度：= [0%]
2022-11-04 14:10:09.117997      回放进度：== [10%]
2022-11-04 14:10:09.127994      回放进度：=== [20%]
2022-11-04 14:10:09.136975      回放进度：==== [30%]
2022-11-04 14:10:09.147919      回放进度：===== [40%]
2022-11-04 14:10:09.159896      回放进度：====== [50%]
2022-11-04 14:10:09.170885      回放进度：======= [60%]
2022-11-04 14:10:09.179832      回放进度：======== [70%]
2022-11-04 14:10:09.189834      回放进度：========= [80%]
2022-11-04 14:10:09.198805      回放进度：========== [90%]
2022-11-04 14:10:09.199786      回放进度：=========== [100%]
2022-11-04 14:10:09.199786      历史数据回放结束
2022-11-04 14:10:09.199786      开始计算逐日盯市盈亏
2022-11-04 14:10:09.214740      逐日盯市盈亏计算完成
2022-11-04 14:10:09.215738      开始计算策略统计指标
2022-11-04 14:10:09.223738      ------------------------------
2022-11-04 14:10:09.223738      首个交易日：    2012-01-18
2022-11-04 14:10:09.223738      最后交易日：    2022-11-03
2022-11-04 14:10:09.224712      总交易日：      2588
2022-11-04 14:10:09.224712      盈利交易日：    76
2022-11-04 14:10:09.224712      亏损交易日：    570
2022-11-04 14:10:09.224712      起始资金：      1,000,000.00
2022-11-04 14:10:09.224712      结束资金：      963,391.67
2022-11-04 14:10:09.225709      总收益率：      -3.66%
2022-11-04 14:10:09.225709      年化收益：      -0.34%
2022-11-04 14:10:09.225709      最大回撤:       -36,608.33
2022-11-04 14:10:09.225709      百分比最大回撤: -3.66%
2022-11-04 14:10:09.225709      最长回撤天数:   3942
2022-11-04 14:10:09.226707      总盈亏：        -36,608.33
2022-11-04 14:10:09.226707      总手续费：      62.33
2022-11-04 14:10:09.226707      总滑点：        35,940.00
2022-11-04 14:10:09.226707      总成交金额：    2,077,626.00
2022-11-04 14:10:09.226707      总成交笔数：    599
2022-11-04 14:10:09.227704      日均盈亏：      -14.15
2022-11-04 14:10:09.227704      日均手续费：    0.02
2022-11-04 14:10:09.227704      日均滑点：      13.89
2022-11-04 14:10:09.227704      日均成交金额：  802.79
2022-11-04 14:10:09.227704      日均成交笔数：  0.23145285935085008
2022-11-04 14:10:09.228701      日均收益率：    -0.00%
2022-11-04 14:10:09.228701      收益标准差：    0.00%
2022-11-04 14:10:09.228701      Sharpe Ratio：  -4.81
2022-11-04 14:10:09.228701      收益回撤比：    -1.00
2022-11-04 14:10:09.230701      策略统计指标计算完成
orders ------------------------------------------------------------
            close_price  pre_close  trade_count  start_pos  end_pos  turnover  commission  slippage  trading_pnl  holding_pnl  total_pnl   net_pnl        balance    return  highlevel     drawdown  ddpercent
date
2012-01-18         9.04       1.00            0          0        0       0.0     0.00000       0.0          0.0          0.0        0.0   0.00000  1000000.00000  0.000000  1000000.0      0.00000   0.000000      
2012-01-19         9.20       9.04            0          0        0       0.0     0.00000       0.0          0.0          0.0        0.0   0.00000  1000000.00000  0.000000  1000000.0      0.00000   0.000000      
2012-01-20         9.42       9.20            0          0        0       0.0     0.00000       0.0          0.0          0.0        0.0   0.00000  1000000.00000  0.000000  1000000.0      0.00000   0.000000      
2012-01-30         9.22       9.42            0          0        0       0.0     0.00000       0.0          0.0         -0.0        0.0   0.00000  1000000.00000  0.000000  1000000.0      0.00000   0.000000      
2012-01-31         9.22       9.22            0          0        0       0.0     0.00000       0.0          0.0          0.0        0.0   0.00000  1000000.00000  0.000000  1000000.0      0.00000   0.000000      
...                 ...        ...          ...        ...      ...       ...         ...       ...          ...          ...        ...       ...            ...       ...        ...          ...        ...      
2022-10-28         6.80       6.82            0          0        0       0.0     0.00000       0.0          0.0         -0.0        0.0   0.00000   963541.85230  0.000000  1000000.0 -36458.14770  -3.645815      
2022-10-31         6.64       6.80            1          0       -1    2019.0     0.06057      60.0         27.0         -0.0       27.0 -33.06057   963508.79173 -0.000034  1000000.0 -36491.20827  -3.649121      
2022-11-01         6.74       6.64            1         -1        0    2004.0     0.06012      60.0         18.0        -30.0      -12.0 -72.06012   963436.73161 -0.000075  1000000.0 -36563.26839  -3.656327      
2022-11-02         6.71       6.74            0          0        0       0.0     0.00000       0.0          0.0         -0.0        0.0   0.00000   963436.73161  0.000000  1000000.0 -36563.26839  -3.656327      
2022-11-03         6.66       6.71            1          0       -1    2013.0     0.06039      60.0         15.0         -0.0       15.0 -45.06039   963391.67122 -0.000047  1000000.0 -36608.32878  -3.660833      

[2588 rows x 17 columns]
trades ------------------------------------------------------------
    gateway_name extra  symbol      exchange orderid tradeid        direction        offset  price  volume                  datetime
0    BACKTESTING  None  600000  Exchange.SSE       1       1  Direction.SHORT   Offset.OPEN   8.36       1 2012-06-11 00:00:00+08:00
1    BACKTESTING  None  600000  Exchange.SSE       2       2   Direction.LONG  Offset.CLOSE   8.30       1 2012-06-14 00:00:00+08:00
2    BACKTESTING  None  600000  Exchange.SSE       3       3  Direction.SHORT   Offset.OPEN   8.06       1 2012-06-27 00:00:00+08:00
3    BACKTESTING  None  600000  Exchange.SSE       4       4   Direction.LONG  Offset.CLOSE   8.05       1 2012-06-28 00:00:00+08:00
4    BACKTESTING  None  600000  Exchange.SSE       5       5  Direction.SHORT   Offset.OPEN   7.67       1 2012-07-10 00:00:00+08:00
..           ...   ...     ...           ...     ...     ...              ...           ...    ...     ...                       ...
594  BACKTESTING  None  600000  Exchange.SSE     595     595  Direction.SHORT   Offset.OPEN   7.01       1 2022-10-12 00:00:00+08:00
595  BACKTESTING  None  600000  Exchange.SSE     596     596   Direction.LONG  Offset.CLOSE   7.03       1 2022-10-13 00:00:00+08:00
596  BACKTESTING  None  600000  Exchange.SSE     597     597  Direction.SHORT   Offset.OPEN   6.73       1 2022-10-31 00:00:00+08:00
597  BACKTESTING  None  600000  Exchange.SSE     598     598   Direction.LONG  Offset.CLOSE   6.68       1 2022-11-01 00:00:00+08:00
598  BACKTESTING  None  600000  Exchange.SSE     599     599  Direction.SHORT   Offset.OPEN   6.71       1 2022-11-03 00:00:00+08:00

[599 rows x 11 columns]
{'annual_return': -0.3394899114064913,
 'capital': 1000000,
 'daily_commission': 0.024083763523956723,
 'daily_net_pnl': -14.14541297527048,
 'daily_return': -0.0014410830764100047,
 'daily_slippage': 13.887171561051005,
 'daily_trade_count': 0.23145285935085008,
 'daily_turnover': 802.7921174652241,
 'end_balance': 963391.67122,
 'end_date': datetime.date(2022, 11, 3),
 'loss_days': 570,
 'max_ddpercent': -3.6608328779999986,
 'max_drawdown': -36608.32877999998,
 'max_drawdown_duration': 3942,
 'profit_days': 76,
 'return_drawdown_ratio': -0.9999999999999998,
 'return_std': 0.004638342749228702,
 'sharpe_ratio': -4.813176651393774,
 'start_date': datetime.date(2012, 1, 18),
 'total_commission': 62.328779999999995,
 'total_days': 2588,
 'total_net_pnl': -36608.32878,
 'total_return': -3.6608328779999977,
 'total_slippage': 35940.0,
 'total_trade_count': 599,
 'total_turnover': 2077626.0}
```