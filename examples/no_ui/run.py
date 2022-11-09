import multiprocessing
import sys
from time import sleep
from datetime import datetime, time
from logging import INFO

from vnpy.event import EventEngine, Event
from vnpy.trader.setting import SETTINGS
from vnpy.trader.engine import MainEngine
from vnpy.trader.object import SubscribeRequest, Exchange, TickData
from vnpy.trader.event import EVENT_TICK
from vnpy.trader.utility import load_json

from vnpy_ctp import CtpGateway
from vnpy_ctp.gateway import ctp_gateway
from vnpy_tts import TtsGateway
from vnpy_ctastrategy import CtaStrategyApp, CtaEngine
from vnpy_ctastrategy.base import EVENT_CTA_LOG

from contracts import IF2303

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True


# ctp_setting = {
#     "用户名": "",
#     "密码": "",
#     "经纪商代码": "",
#     "交易服务器": "",
#     "行情服务器": "",
#     "产品名称": "",
#     "授权编码": "",
#     "产品信息": ""
# }

GATEWAYS = {
    "TTS": TtsGateway,
    "CTP": CtpGateway
}

SETTING_FILE = {
    "TTS": "tts_setting.json",
    "CTP": "ctp_setting.json"
}


def load_strategy(filename: str):
    import json
    with open(filename) as f:
        return json.load(f)


# Chinese futures market trading period (day/night)
DAY_START = time(8, 45)
DAY_END = time(15, 0)

NIGHT_START = time(20, 45)
NIGHT_END = time(2, 45)


def check_trading_period():
    """"""
    current_time = datetime.now().time()

    trading = False
    if (
        (current_time >= DAY_START and current_time <= DAY_END)
        or (current_time >= NIGHT_START)
        or (current_time <= NIGHT_END)
    ):
        trading = True

    return trading


def run_engine(gateway: str="CTP", strategies: dict=None):
    """
    Running in the child process.
    """
    SETTINGS["log.file"] = True

    with open(SETTING_FILE[gateway], encoding="utf-8") as f:
        import json
        ctp_setting = json.load(f)
        print(ctp_setting)

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(GATEWAYS[gateway])
    # main_engine.add_gateway(CtpGateway)
    cta_engine: CtaEngine = main_engine.add_app(CtaStrategyApp)
    main_engine.write_log("主引擎创建成功")

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")

    main_engine.connect(ctp_setting, gateway)
    main_engine.write_log("连接CTP接口")
    # ctp: CtpGateway = main_engine.gateways[gateway]
    
    cta_engine.load_strategy_class_from_module("mystg.empty_stg")
    cta_engine.init_engine()
    main_engine.write_log("CTA策略初始化完成")
    cta_engine.main_engine.engines["oms"].contracts[IF2303.vt_symbol] = IF2303

    if not strategies:
        strategies = {}
    for name, config in strategies.items():
        print("add", name, config)
        cta_engine.add_strategy(config["class_name"], name, config["vt_symbol"], config["setting"])

    for name in strategies:
        print("init", name)
        cta_engine.init_strategy(name)
    # cta_engine.init_all_strategies()
    
    sleep(10)   # Leave enough time to complete strategy initialization
    main_engine.write_log("CTA策略全部初始化")

    cta_engine.start_all_strategies()
    main_engine.write_log("CTA策略全部启动")
    return main_engine


def scan_loop(main_engine: MainEngine, check=True):

    while True:
        sleep(10)

        if check:
            trading = check_trading_period()
            if not trading:
                print("关闭子进程")
                main_engine.close()
                sys.exit(0)
            print("trading")
        else:
            print("trading")


def run_child():

    engine = run_engine()
    scan_loop(engine)


def on_tick(event: Event):
    print("on tick", event.data)


def run_interuptable(gateway: str="CTP", strategies: dict=None):
    try:
        engine: MainEngine = run_engine(gateway, strategies)
        # engine.event_engine.register(EVENT_TICK, on_tick)
        # print(engine.event_engine._handlers[EVENT_TICK])
        # engine.subscribe(SubscribeRequest(IF2303.symbol, IF2303.exchange), gateway)

        scan_loop(engine, False)
    
    finally:
        print("Finally: KeyBoardInterrupt")
        engine.close()
        print("end")
        sys.exit(0)



def run_parent():
    """
    Running in the parent process.
    """
    print("启动CTA策略守护父进程")

    child_process = None

    while True:
        trading = check_trading_period()

        # Start child process in trading period
        if trading and child_process is None:
            print("启动子进程")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("子进程启动成功")

        # 非记录时间则退出子进程
        if not trading and child_process is not None:
            if not child_process.is_alive():
                child_process = None
                print("子进程关闭成功")

        sleep(5)


if __name__ == "__main__":
    # run_parent()
    strategies = load_strategy("cta_strategy_setting.json")
    print(strategies)
    run_interuptable(strategies=strategies)
