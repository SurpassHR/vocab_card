import os
import sqlite3
import json
from typing import List, Optional
from utils.date_utils import dateStringToTimestamp, DatePosition
from utils.config_utils import Config
from utils.public_def import RESULT, MEANING, ITEM, CONFIG_FILE
from utils.logger import Logger

DEBUG_FLG = False

class PotAppWordHistoryBD:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name
        self.logger = Logger(__name__).getLogger()
        try:
            self.cur = sqlite3.connect(db_name).cursor()
            self.logger.info(f"connect to db: {self.db_name} succ.")
        except:
            self.logger.error(f"connect to db: {self.db_name} failed.")

    def procDBParse(self, startDateTimestamp: int, endDateTimestamp: int) -> Optional[List[dict]]:
        res = self._getCambDictDataFromSqlDBByData(startDateTimestamp, endDateTimestamp)
        res_dict = {}
        for item in res:
            structured_result = self._parseResult(item['text'], item['result'])
            if structured_result is None:
                continue
            if DEBUG_FLG:
                # self._formatResult(structured_result)
                pass
            else:
                vocab_dict = self._formatOutput(structured_result)
                if vocab_dict:
                    res_dict[vocab_dict['word']] = vocab_dict

        return list(res_dict.values())

    # 获取历史数据数量
    def _getDataNumFromSqlDB(self) -> int:
        history_num = self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()
        if history_num is not None:
            history_num = history_num[0]
        return history_num

    # 获取数据库表头
    def _getTitleFromSqlDB(self) -> List[str]:
        column_names = self.cur.execute(f"PRAGMA table_info({self.table_name})").fetchall()
        return column_names

    def _extractNewDBFromOriginDBByTimeRange(self, startTime: str, endTime: str, new_db_name: str) -> bool:
        try:
            # 获取原表结构
            create_table_row = self.cur.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                (self.table_name,)
            ).fetchone()
            if not create_table_row:
                self.logger.error(f"原表 {self.table_name} 不存在")
                return False
            create_table_sql = create_table_row[0]

            # 上级目录不存在时创建目录
            if not os.path.exists(os.path.dirname(new_db_name)):
                os.makedirs(os.path.dirname(new_db_name))

            # 创建新数据库连接
            new_conn = sqlite3.connect(new_db_name)
            new_cur = new_conn.cursor()

            # 处理表存在的情况
            new_cur.execute(f"DROP TABLE IF EXISTS {self.table_name}")  # 先删除旧表
            new_cur.execute(create_table_sql)  # 按原结构重建表

            # 获取原表列名
            self.cur.execute(f"PRAGMA table_info({self.table_name})")
            columns = [row[1] for row in self.cur.fetchall()]
            # self.logger.debug(columns) # ['id', 'text', 'source', 'target', 'service', 'result', 'timestamp']

            # 准备插入语句
            placeholders = ','.join(['?'] * len(columns))
            insert_sql = f"INSERT INTO {self.table_name} ({','.join(columns)}) VALUES ({placeholders})"

            # 获取数据
            startTimestamp = dateStringToTimestamp(startTime, DatePosition.LEFT_SIDE)
            endTimestamp = dateStringToTimestamp(endTime, DatePosition.RIGHT_SIDE)
            self.logger.info(f"{startTime}, {startTimestamp}, {endTime}, {endTimestamp}")
            data = self._getCambDictDataFromSqlDBByData(
                startTimestamp=startTimestamp,
                endTimestamp=endTimestamp
            )
            if not data:
                self.logger.info("没有需要导出的数据")
                new_conn.close()
                return False

            # 批量插入数据
            data_values = []
            for item in data:
                row_values = []
                for col in columns:
                    col_data = item.get(col) # 使用 get(col) 而不是 get(col, None) 以区分不存在的键和值为None的情况，虽然在这里影响不大

                    # 处理 result 列
                    if col == 'result' and col_data != '':
                        try:
                            json_col_data = json.loads(col_data)

                            # 确保 'pronunciations' 和 voice 存在且不为空
                            pronunciations = json_col_data.get('pronunciations')
                            voice_data = pronunciations[0].get('voice')
                            if voice_data: # 检查 voice_data 是否非空
                                for pronoun in pronunciations:
                                    pronoun['voice'] = []
                                    # 注意：这里只修改了第一个发音项的 voice，如果可能有多个发音项需要处理，逻辑需调整
                            # 使用 json.dumps 保证是有效的 JSON 字符串
                            json_col_data['pronunciations'] = pronunciations
                            col_data = json.dumps(json_col_data)
                        except (json.JSONDecodeError, TypeError, KeyError, IndexError) as e:
                            self.logger.error(f"处理 result 列时出错: {e}, row data: {item}")
                            # 可以选择跳过这行，或者将 result 设为 None 或错误标记
                            col_data = None # 或者保持原样，或者记录错误

                    # 直接添加获取到的值，包括 None
                    row_values.append(col_data)

                # 确保列的数量匹配（理论上应该总是匹配，除非原始数据有问题）
                if '' in row_values:
                    self.logger.warning(f"警告：包含空数据{row_values}")
                    pass
                elif len(row_values) != len(columns):
                    self.logger.warning(f"警告：跳过一行，因为列数不匹配 ({len(row_values)} vs {len(columns)}")
                    pass
                else:
                    data_values.append(tuple(row_values))

            self.logger.info(f"sync data from {self.db_name} to {new_db_name}, range: {startTime} - {endTime}, data num: {len(data_values)}")
            new_cur.executemany(insert_sql, data_values)
            new_conn.commit()
            new_conn.close()
            return True
        except Exception as e:
            self.logger.error(f"导出数据失败: {e}")
            if 'new_conn' in locals():
                new_conn.rollback()
                new_conn.close()
            return False

    def _getCambDictDataFromSqlDBByData(self, startTimestamp: int, endTimestamp: int) -> List[ITEM]:
        try:
            res = self.cur.execute(f"SELECT * FROM {self.table_name} WHERE service = 'cambridge_dict' AND timestamp >= {startTimestamp} AND timestamp <= {endTimestamp}").fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Error: {e}")
            return []

        struct_list = [ITEM(*item) for item in res]
        dict_list = []
        [dict_list.append(item._asdict()) for item in struct_list if len(item._asdict().keys()) == 7]

        return dict_list

    def _parseResult(self, text:str, result_str: str) -> RESULT:
        try:
            parsed_res = json.loads(result_str)
        except:
            return

        result = RESULT(
            text=text,
            region=[],
            symbol=[],
            meaning=[],
        )

        def _appendListItem(result, item_name: str, res_item) -> None:
            local_res_item = res_item
            if isinstance(local_res_item, list):
                local_res_item = local_res_item[0]
            if res_item is not None:
                method = getattr(result, item_name).append
                method(local_res_item)

        # 提取发音信息
        pronunciations = parsed_res.get("pronunciations", [])
        for pron in pronunciations:
            region = pron.get("region")
            _appendListItem(result, 'region', region)

            symbol = pron.get("symbol")
            _appendListItem(result, 'symbol', symbol)

            _ = pron.get("voice", [])

        # 提取解释信息
        explanations = parsed_res.get("explanations", [])
        for exp in explanations:
            try:
                meaning = MEANING(
                    mean=exp.get("meaning"),
                    trait=exp.get("trait"),
                    explain=exp.get("explain"),
                    exampleEn=[],
                    exampleZh=[],
                )
            except:
                continue
            examplesEn = exp.get("exampleEn", [])
            for example in examplesEn:
                _appendListItem(meaning, 'exampleEn', example)

            examplesZh = exp.get("exampleZh", [])
            for example in examplesZh:
                _appendListItem(meaning, 'exampleZh', example)

            _appendListItem(result, 'meaning', meaning)

        return result

    def _formatResult(self, result: RESULT) -> None:
        self.logger.info(f"生词: {result.text}")
        for r, s in zip(result.region, result.symbol):
            self.logger.info(f"  - {r}: {s}")

        self.logger.info("释义: ")
        meaningList: List[MEANING] = result.meaning
        for meaning in  meaningList:
            self.logger.info(f"  - {meaning.mean} - {meaning.trait}: {meaning.explain}")

        self.logger.info("例句:")
        for meaning in meaningList:
            self.logger.info(f"  - {meaning.exampleEn} - {meaning.exampleZh}")

        self.logger.debug('\n')

    def _formatOutput(self, result: RESULT) -> Optional[dict]:
        vocab_dict = {
            'word': result.text,
            'pronounce': [],
            'meaning': {}
        }

        for r, s in zip(result.region, result.symbol):
            vocab_dict['pronounce'].append({'region': r, 'symbol': s})

        for mean in result.meaning:
            if mean.mean:
                if isinstance(mean.mean, list):
                    for m in mean.mean:
                        vocab_dict['meaning'][m] = {'trait': mean.trait, 'explain': mean.explain, 'exampleEn': mean.exampleEn, 'exampleZh': mean.exampleZh}
                elif isinstance(mean.mean, str):
                    vocab_dict['meaning'][mean.mean] = {'trait': mean.trait, 'explain': mean.explain, 'exampleEn': mean.exampleEn, 'exampleZh': mean.exampleZh}

        return vocab_dict

if __name__ == '__main__':
    config_mgr = Config(CONFIG_FILE)
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")

    pot_db = PotAppWordHistoryBD(db_name=db_name, table_name=table_name)
    ret = pot_db.procDBParse(
        dateStringToTimestamp(
            date_str='25-03-01',
            date_position=DatePosition.LEFT_SIDE
        ),
        dateStringToTimestamp(
            date_str='25-04-21',
            date_position=DatePosition.RIGHT_SIDE
        )
    )