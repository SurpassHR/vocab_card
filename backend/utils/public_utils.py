from typing import List
import json

# list 去重
def list_dedup(in_list) -> List:
    seen = set()
    result = []
    for d in in_list:
        d_str = json.dumps(d, sort_keys=True)  # 转字符串去重
        if d_str not in seen:
            seen.add(d_str)
            result.append(d)
    return result