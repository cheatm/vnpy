from vnpy.trader.object import (
    TickData,
    OrderData,
    TradeData,
    PositionData,
    AccountData,
    ContractData,
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
)
from vnpy.trader.constant import (
    Direction,
    Offset,
    Exchange,
    OrderType,
    Product,
    Status,
    OptionType
)


IF2303 = ContractData(
    name="股指2303",
    gateway_name="CTP",
    symbol="IF2303",
    exchange=Exchange.CFFEX,
    product=Product.FUTURES,
    size=300,
    pricetick=0.2,
    min_volume=1
)