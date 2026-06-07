from datetime import datetime
import pytz
from app.core.config import Config

def now():
    tz = pytz.timezone(Config.APP_TIMEZONE)
    return datetime.now(tz)

def utc_now():
    return datetime.utcnow()