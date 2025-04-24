import datetime
import tzlocal
from enum import Enum
from datetime import datetime, timedelta

class DatePosition(Enum):
    LEFT_SIDE = 0
    RIGHT_SIDE = 1

MILLISECS_IN_A_DAY = 86400000
YEARS_IN_A_CENTURY = 100
CURRENT_CENTURY_YEAR_BASE = 2000
MILLISECS_IN_A_SEC = 1000

def getLocalMillisecsOffsetFromUtc() -> int:
    # 获取本地时区对象
    local_tz = tzlocal.get_localzone()
    # 获取当前时间
    now = datetime.now(local_tz)
    # 获取 UTC 偏移量
    utc_offset = local_tz.utcoffset(now)
    # 获取偏移量的总秒数
    return int(utc_offset.total_seconds() * 1000)

def matchProcDateString(date_str: str) -> int:
    date_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%y-%m-%d",
    ]
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(date_str, date_format)
        except:
            continue

        # 处理简写年
        if "%y" in date_format and date_obj.year < YEARS_IN_A_CENTURY:
            date_obj = date_obj.replace(year=date_obj.year + CURRENT_CENTURY_YEAR_BASE)
        return int(date_obj.timestamp() * MILLISECS_IN_A_SEC)

    return 0

def dateStringToTimestamp(date_str: str, date_position: DatePosition) -> int:
    time_stamp = matchProcDateString(date_str)
    if time_stamp != 0:
        # 取当前整数天
        time_stamp -= (time_stamp + getLocalMillisecsOffsetFromUtc()) % MILLISECS_IN_A_DAY

    # left/right 定义，左闭右开
    if date_position is DatePosition.LEFT_SIDE:
        pass
    elif date_position is DatePosition.RIGHT_SIDE:
        time_stamp += MILLISECS_IN_A_DAY - 1

    return time_stamp

def fromTimestampToStr(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp / MILLISECS_IN_A_SEC).strftime("%Y-%m-%d %H:%M:%S")

def getCurrTime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getCurrTimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)

def getLastYesterdaySecTimestamp() -> int:
    now = datetime.now()
    yesterday = now - timedelta(days=0)
    yesterday_235959 = yesterday.replace(hour=23, minute=59, second=59, microsecond=999)
    timestamp = yesterday_235959.timestamp()

    return int(timestamp * 1000) # 精确到毫秒

if __name__ == '__main__':
    date_str = '25-02-26'