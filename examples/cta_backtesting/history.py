from vnpy.trader import setting
from vnpy_datamanager.engine import ManagerEngine, MainEngine
from vnpy.trader.constant import Exchange
from vnpy_sqlite import sqlite_database
from datetime import datetime


# datafeed
setting.SETTINGS["datafeed.name"] = "tushare"
setting.SETTINGS["datafeed.username"] = "13823156147"
setting.SETTINGS["datafeed.password"] = "8463f1ce666d4b560ab339c087efc2137d16347b91f767d05bc57037"

# database
setting.SETTINGS["database.name"] = "sqlite"
setting.SETTINGS["database.database"] = "database.db"


def test_download(manager: ManagerEngine):

    result = manager.download_bar_data(
        symbol="600000",
        exchange=Exchange.SSE,
        interval="d",
        start=datetime(2012, 1, 1)
    )

    print("download result", result)

def test():
    me = MainEngine()
    
    manager = ManagerEngine(me, me.event_engine)
    
    try:
        test_download(manager)
    
    finally:
        
        manager.event_engine.stop()
        manager.main_engine.close()


def main():
    
    test()


if __name__ == "__main__":
    main()