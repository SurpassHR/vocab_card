import sqlite3
import json
from datetime import datetime, timedelta
from collections import namedtuple
from typing import List, Optional
from utils.config_utils import Config

ITEM = namedtuple('Item', ['id', 'text', 'source', 'target', 'service', 'result', 'timestamp'])
RESULT = namedtuple('Result', ['text', 'region', 'symbol', 'trait', 'meaning', 'explain', 'exampleZh', 'exampleEn'])
DEBUG_FLG = False

class PotAppWordHistoryBD:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name
        try:
            self.cur = sqlite3.connect(db_name).cursor()
        except:
            print("connect to db failed.")

    def procDBParse(self, date: str) -> Optional[List[dict]]:
        res = self._getCambDictDataFromSqlDBByData(date)
        res_list = []
        for item in res:
            structured_result = self._parseResult(item['text'], item['result'])
            if structured_result is None:
                continue
            if DEBUG_FLG:
                return self._formatResult(structured_result)
            else:
                self._formatResult(structured_result)
                res_list.append(self._formatOutput(structured_result))
        return res_list

    # 获取历史数据数量
    def _getDataNumFromSqlDB(self) -> int:
        history_num = self.cur.execute(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()
        if history_num is not None:
            history_num = history_num[0]
        # print(history_num)
        return history_num

    # 获取数据库表头
    def _getTitleFromSqlDB(self) -> List[str]:
        column_names = self.cur.execute(f"PRAGMA table_info({self.table_name})").fetchall()
        return column_names

    def _getCambDictDataFromSqlDBByData(self, date: str) -> ITEM:
        res = self.cur.execute(f"SELECT * FROM {self.table_name} WHERE service = \'cambridge_dict\' AND timestamp < \'{date}\' AND timestamp >= \'{date - 86400000}\' ORDER BY id DESC LIMIT 20 OFFSET 0").fetchall()
        struct_list = [ITEM(*item) for item in res]
        dict_list = [item._asdict() for item in struct_list]
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
            trait=[],
            meaning=[],
            explain=[],
            exampleZh=[],
            exampleEn=[]
        )

        def _appendResult(result: RESULT, item_name: str, res_item: str) -> None:
            local_res_item = res_item
            if isinstance(local_res_item, list):
                local_res_item = local_res_item[0]
            if res_item is not None:
                method = getattr(result, item_name).append
                method(str(local_res_item))

        # 提取发音信息
        pronunciations = parsed_res.get("pronunciations", [])
        for pron in pronunciations:
            region = pron.get("region")
            _appendResult(result, 'region', region)

            symbol = pron.get("symbol")
            _appendResult(result, 'symbol', symbol)

            _ = pron.get("voice", [])

        # 提取解释信息
        explanations = parsed_res.get("explanations", [])
        for exp in explanations:
            trait = exp.get("trait")
            _appendResult(result, 'trait', trait)

            meaning = exp.get("meaning")
            _appendResult(result, 'meaning', meaning)

            explain = exp.get("explain")
            _appendResult(result, 'explain', explain)

            exampleZh = exp.get("exampleZh")
            _appendResult(result, 'exampleZh', exampleZh)

            exampleEn = exp.get("exampleEn")
            _appendResult(result, 'exampleEn', exampleEn)

        return result

    def _formatResult(self, result: RESULT) -> None:
        print(f"生词: {result.text}")
        for r, s in zip(result.region, result.symbol):
            print(f"  - {r}: {s}")

        print("释义: ")
        for t, m, e in zip(result.trait, result.meaning, result.explain):
            print(f"  - {e} - {m}, {t}")

        print("例句:")
        for zh, en in zip(result.exampleZh, result.exampleEn):
            print(f"  - {en} - {zh}")

        print('\n')

    def _formatOutput(self, result: RESULT) -> Optional[dict]:
        vocab_dict = {
            'word': result.text,
            'pronounce': [],
            'explanations': [],
            'example': []
        }

        for r, s in zip(result.region, result.symbol):
            vocab_dict['pronounce'].append({'region': r, 'symbol': s})

        for t, m, e in zip(result.trait, result.meaning, result.explain):
            vocab_dict['explanations'].append({'trait': t, 'meaning': m, 'explain': e})

        for en, zh in zip(result.exampleEn, result.exampleZh):
            vocab_dict['example'].append({'exampleEn': en, 'exampleZh': zh})

        return vocab_dict

def getLastYesterdaySecTimestamp() -> int:
    now = datetime.now()
    yesterday = now - timedelta(days=0)
    yesterday_235959 = yesterday.replace(hour=23, minute=59, second=59, microsecond=999)
    timestamp = yesterday_235959.timestamp()
    # print(int(timestamp * 1000))

    return int(timestamp * 1000) # 精确到毫秒

if __name__ == '__main__':
    DEBUG_FLG = True

    config_mgr = Config("utils/config.yaml")
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")

    pot_db = PotAppWordHistoryBD(db_name=db_name, table_name=table_name)
    yesterday = getLastYesterdaySecTimestamp()
    pot_db.procDBParse(yesterday)