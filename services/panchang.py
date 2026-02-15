from suncalc import get_times
from datetime import datetime, timedelta
import pytz


IST = pytz.timezone("Asia/Kolkata")


async def calculate_choghadiya(date_obj, lat, lng):

    date_dt = datetime.combine(date_obj, datetime.min.time())

    sun = get_times(date_dt, lat, lng)

    sunrise = sun["sunrise"].astimezone(IST)
    sunset = sun["sunset"].astimezone(IST)

    # next day sunrise
    next_day = date_dt + timedelta(days=1)
    next_sun = get_times(next_day, lat, lng)
    next_sunrise = next_sun["sunrise"].astimezone(IST)

    # durations
    day_duration = sunset - sunrise
    night_duration = next_sunrise - sunset

    def generate_segments(start, duration):
        segment = duration / 8
        return [
            {
                "start_time": (start + segment * i).strftime("%H:%M:%S"),
                "end_time": (start + segment * (i + 1)).strftime("%H:%M:%S"),
                "type": "Segment"
            }
            for i in range(8)
        ]

    return {
        "sunrise": sunrise.strftime("%H:%M:%S"),
        "sunset": sunset.strftime("%H:%M:%S"),
        "day_choghadiya": generate_segments(sunrise, day_duration),
        "night_choghadiya": generate_segments(sunset, night_duration),
    }
