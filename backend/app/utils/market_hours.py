from datetime import datetime, time
import pytz

EASTERN = pytz.timezone("US/Eastern")

def get_market_status() -> dict:
    now_et = datetime.now(EASTERN)
    weekday = now_et.weekday()  # 0=Mon, 6=Sun
    current_time = now_et.time()

    if weekday >= 5:  # Weekend
        return {"is_open": False, "session": "closed", "timezone": "US/Eastern"}

    pre_open = time(4, 0)
    market_open = time(9, 30)
    market_close = time(16, 0)
    after_close = time(20, 0)

    if market_open <= current_time < market_close:
        return {"is_open": True, "session": "regular", "timezone": "US/Eastern"}
    elif pre_open <= current_time < market_open:
        return {"is_open": False, "session": "pre", "timezone": "US/Eastern"}
    elif market_close <= current_time < after_close:
        return {"is_open": False, "session": "after", "timezone": "US/Eastern"}
    else:
        return {"is_open": False, "session": "closed", "timezone": "US/Eastern"}

def is_market_open() -> bool:
    return get_market_status()["is_open"]
