import datetime
import time

def date_string_to_timestamp(date_str):
    """
    自动判断日期字符串格式并转换为时间戳。
        date_str (str): 日期字符串。

    Returns:
        int: 时间戳（秒），如果无法解析日期字符串则返回 None。
    """
    date_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%y-%m-%d %H:%M:%S",
    ]

    date_formats_inc = [
        "%Y-%m-%d",
        "%y-%m-%d",
    ]

    for date_format in date_formats:
        try:
            date_obj = datetime.datetime.strptime(date_str, date_format)
            # 处理两位数年份
            if "%y" in date_format and date_obj.year < 100:
                date_obj = date_obj.replace(year=date_obj.year + 2000)
            return int(date_obj.timestamp() * 1000)
        except ValueError:
            continue

    for date_format in date_formats_inc:
        try:
            date_obj = datetime.datetime.strptime(date_str, date_format)
            # 处理两位数年份
            if "%y" in date_format and date_obj.year < 100:
                date_obj = date_obj.replace(year=date_obj.year + 2000)
            return int(date_obj.timestamp() * 1000) + 86399000
        except ValueError:
            continue

    return None

def from_timestamp_to_str(timestamp: int) -> str:
    return datetime.datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")