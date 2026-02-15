from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

from .muhurat_service import get_shubh_muhurats

TIMEZONE = "Asia/Kolkata"


def get_current_month_muhurats():
    tz = pytz.timezone(TIMEZONE)

    today = datetime.now(tz)
    start = today.replace(day=1)
    end = start + relativedelta(months=1)

    results = []
    current = start

    while current < end:
        results.append(get_shubh_muhurats(current))
        current += timedelta(days=1)

    return results
