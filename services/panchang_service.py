from datetime import datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun

TIMEZONE = "Asia/Kolkata"

# India standard reference (Ujjain Panchang reference)
LAT = 23.1765
LON = 75.7885


def get_sun_times(date):
    """Get sunrise and sunset"""
    city = LocationInfo("India", "India", TIMEZONE, LAT, LON)
    s = sun(city.observer, date=date)

    return s["sunrise"], s["sunset"]


def get_day_segments(sunrise, sunset):
    """Divide day into 8 equal parts"""
    duration = (sunset - sunrise) / 8

    segments = []
    for i in range(8):
        start = sunrise + duration * i
        end = start + duration
        segments.append((start, end))

    return segments


# weekday mapping (0=Monday)
RAHU_MAP = [1, 6, 4, 5, 3, 2, 7]
YAMAGANDA_MAP = [4, 3, 2, 1, 0, 6, 5]
GULIKA_MAP = [6, 5, 4, 3, 2, 1, 0]


def format_time(start, end):
    return f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"


def calculate_abhijit(sunrise, sunset):
    """Abhijit Muhurat (midday)"""
    midday = sunrise + (sunset - sunrise) / 2

    start = midday - timedelta(minutes=24)
    end = midday + timedelta(minutes=24)

    return format_time(start, end)


def get_shubh_muhurats(date: datetime):
    tz = pytz.timezone(TIMEZONE)

    if date.tzinfo is None:
        date = tz.localize(date)

    sunrise, sunset = get_sun_times(date.date())
    segments = get_day_segments(sunrise, sunset)

    weekday = date.weekday()

    rahu = segments[RAHU_MAP[weekday]]
    yamaganda = segments[YAMAGANDA_MAP[weekday]]
    gulika = segments[GULIKA_MAP[weekday]]

    return {
        "date": date.strftime("%Y-%m-%d"),
        "sunrise": sunrise.strftime("%H:%M"),
        "sunset": sunset.strftime("%H:%M"),
        "abhijit_muhurat": calculate_abhijit(sunrise, sunset),
        "rahu_kaal": format_time(*rahu),
        "yamaganda": format_time(*yamaganda),
        "gulika_kaal": format_time(*gulika),
    }
