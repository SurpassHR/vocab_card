from potapp_db import PotAppWordHistoryBD
from utils.config_utils import Config
from utils.date_utils import getCurrTime
from utils.public_def import CONFIG_FILE

if __name__ == '__main__':
    print(CONFIG_FILE)
    config_mgr = Config(CONFIG_FILE)
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")

    pot_db = PotAppWordHistoryBD(db_name=db_name, table_name=table_name)

    sync_config = config_mgr.get("database.sync_config")
    start_time = sync_config.get("start_time", "2023-01-01 00:00:00")
    start_time = "2023-01-01 00:00:00" if start_time == '' else start_time
    # 如果没有设置结束时间，则默认使用当前时间
    end_time = sync_config.get("end_time", getCurrTime())
    end_time = getCurrTime() if end_time == '' else end_time

    # 按照时间范围导出不包含音频数据的数据库，后缀使用txt是为了同步时以字符diff进行同步
    pot_db._extractNewDBFromOriginDBByTimeRange(start_time, end_time, 'output/syncDB.db')
