import pytest
from datetime import datetime
from weather_mcp.services.time import TimeService
from weather_mcp.exceptions import InvalidParameterError

def test_get_current_datetime():
    service = TimeService()
    dt_str = service.get_current_datetime("UTC")
    assert isinstance(dt_str, str)
    # Check if string is in ISO format
    dt = datetime.fromisoformat(dt_str)
    assert dt.tzinfo is not None

def test_get_timezone_info():
    service = TimeService()
    info = service.get_timezone_info("Asia/Shanghai")
    assert info["timezone"] == "Asia/Shanghai"
    assert "offset" in info
    assert "is_dst" in info
    assert "name" in info

def test_convert_time():
    service = TimeService()
    # 2023-01-01 12:00:00 UTC -> 2023-01-01 20:00:00 Asia/Shanghai (UTC+8)
    time_str = "2023-01-01T12:00:00+00:00"
    converted = service.convert_time(time_str, "UTC", "Asia/Shanghai")
    assert converted == "2023-01-01T20:00:00+08:00"

def test_invalid_timezone():
    service = TimeService()
    with pytest.raises(InvalidParameterError):
        service.get_current_datetime("Invalid/Timezone")
