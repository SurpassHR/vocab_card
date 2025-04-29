import os

from potapp_db import PotAppWordHistoryBD
from utils.config_utils import Config
from utils.date_utils import getCurrTime
from utils.public_def import CONFIG_FILE

if __name__ == '__main__':
    print(CONFIG_FILE)
    config_mgr = Config(CONFIG_FILE)
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")

    sync_config = config_mgr.get("database.sync_config")
    start_time = sync_config.get("start_time")
    start_time = "2023-01-01 00:00:00" if not start_time or start_time == "" else start_time
    # 如果没有设置结束时间，则默认使用当前时间
    end_time = sync_config.get("end_time")
    end_time = getCurrTime() if not end_time or end_time == "" else end_time
    # 获取同步数据的源数据库和目标数据库
    src_database = sync_config.get("src_database")
    src_database = db_name if not src_database or src_database == "" else src_database
    dst_database = sync_config.get("dst_database")
    dst_database = os.path.join('output', 'syncDB.db') if not dst_database or dst_database == "" else dst_database

    pot_db = PotAppWordHistoryBD(
        db_name=src_database,
        table_name=table_name
    )

    # 按照时间范围导出不包含音频数据的数据库，后缀使用txt是为了同步时以字符diff进行同步
    pot_db._extractNewDBFromOriginDBByTimeRange(
        startTime=start_time,
        endTime=end_time,
        dstDBName=dst_database
    )
