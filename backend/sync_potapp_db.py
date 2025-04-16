from potapp_db import PotAppWordHistoryBD
from utils.config_utils import Config

if __name__ == '__main__':
    from utils.public_def import CONFIG_FILE
    DEBUG_FLG = True

    config_mgr = Config(CONFIG_FILE)
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")

    pot_db = PotAppWordHistoryBD(db_name=db_name, table_name=table_name)

    # 按照时间范围导出不包含音频数据的数据库，后缀使用txt是为了同步时以字符diff进行同步
    pot_db._extractNewDBFromOriginDBByTimeRange('2025-03-01', '2025-04-16', 'syncDB.db')