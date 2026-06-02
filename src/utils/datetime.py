
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def format_time(dt: datetime, time_zone: str, fmt: str = "%H:%M:%S %d-%m-%Y") -> str :
    ''' Format datetime in local timezone '''
    tz = ZoneInfo(time_zone)
    return dt.astimezone(tz).strftime(fmt)
