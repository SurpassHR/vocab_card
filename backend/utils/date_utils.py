import datetime
from enum import EnumType
import tzlocal

class DatePosition(EnumType):
    LEFT_SIDE = 0
    RIGHT_SIDE = 1

MILLISECS_IN_A_DAY = 86400000
YEARS_IN_A_CENTURY = 100
CURRENT_CENTURY_YEAR_BASE = 2000
MILLISECS_IN_A_SEC = 1000

def get_local_millisecs_offset_from_utc() -> int:
    # 获取本地时区对象
    local_tz = tzlocal.get_localzone()
    # 获取当前时间
    now = datetime.datetime.now(local_tz)
    # 获取 UTC 偏移量
    utc_offset = local_tz.utcoffset(now)
    # 获取偏移量的总秒数
    return int(utc_offset.total_seconds() * 1000)

def match_proc_date_string(date_str: str) -> int:
    date_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%y-%m-%d",
    ]
    for date_format in date_formats:
        try:
            date_obj = datetime.datetime.strptime(date_str, date_format)
        except:
            continue

        # 处理简写年
        if "%y" in date_format and date_obj.year < YEARS_IN_A_CENTURY:
            date_obj = date_obj.replace(year=date_obj.year + CURRENT_CENTURY_YEAR_BASE)
        return int(date_obj.timestamp() * MILLISECS_IN_A_SEC)

    return 0

def date_string_to_timestamp(date_str: str, date_position: DatePosition) -> int:
    time_stamp = match_proc_date_string(date_str)
    if time_stamp != 0:
        # 取当前整数天
        time_stamp -= (time_stamp + get_local_millisecs_offset_from_utc()) % MILLISECS_IN_A_DAY

    # left/right 定义，左闭右开
    if date_position is DatePosition.LEFT_SIDE:
        pass
    elif date_position is DatePosition.RIGHT_SIDE:
        time_stamp += MILLISECS_IN_A_DAY - 1

    return time_stamp

def from_timestamp_to_str(timestamp: int) -> str:
    return datetime.datetime.fromtimestamp(timestamp / MILLISECS_IN_A_SEC).strftime("%Y-%m-%d %H:%M:%S")