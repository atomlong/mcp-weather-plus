from datetime import datetime
import pytz
from typing import Dict, Any
from weather_mcp.exceptions import InvalidParameterError

class TimeService:
    def get_current_datetime(self, timezone_name: str) -> str:
        try:
            tz = pytz.timezone(timezone_name)
            return datetime.now(tz).isoformat()
        except pytz.UnknownTimeZoneError:
            raise InvalidParameterError(f"Unknown timezone: {timezone_name}")

    def get_timezone_info(self, timezone_name: str) -> Dict[str, Any]:
        try:
            tz = pytz.timezone(timezone_name)
            now = datetime.now(tz)
            return {
                "timezone": timezone_name,
                "offset": now.strftime("%z"),
                "is_dst": bool(now.dst()),
                "name": now.tzname()
            }
        except pytz.UnknownTimeZoneError:
            raise InvalidParameterError(f"Unknown timezone: {timezone_name}")

    def convert_time(self, time_str: str, from_timezone: str, to_timezone: str) -> str:
        try:
            from_tz = pytz.timezone(from_timezone)
            to_tz = pytz.timezone(to_timezone)
            
            # Parse time string. Assume ISO format.
            try:
                dt = datetime.fromisoformat(time_str)
            except ValueError:
                raise InvalidParameterError(f"Invalid time format: {time_str}. Expected ISO format.")

            if dt.tzinfo is None:
                dt = from_tz.localize(dt)
            else:
                dt = dt.astimezone(from_tz)
                
            return dt.astimezone(to_tz).isoformat()
        except pytz.UnknownTimeZoneError as e:
            raise InvalidParameterError(f"Unknown timezone: {str(e)}")
