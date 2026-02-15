from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz


# Day sequences based on weekday
# 0 = Monday ... 6 = Sunday (python weekday)
DAY_SEQUENCES = {
    6: ["Udveg", "Chal", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"],  # Sunday
    0: ["Amrit", "Chal", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit"],  # Monday
    1: ["Rog", "Udveg", "Chal", "Labh", "Amrit", "Kaal", "Shubh", "Rog"],    # Tuesday
    2: ["Labh", "Udveg", "Chal", "Amrit", "Kaal", "Shubh", "Rog", "Labh"],   # Wednesday
    3: ["Shubh", "Rog", "Udveg", "Chal", "Labh", "Amrit", "Kaal", "Shubh"],  # Thursday
    4: ["Chal", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Chal"],   # Friday
    5: ["Kaal", "Shubh", "Rog", "Udveg", "Chal", "Labh", "Amrit", "Kaal"],   # Saturday
}


def split_into_8_parts(start, end, sequence):
    """Split duration into 8 parts and assign choghadiya names"""
    duration = (end - start) / 8
    slots = []

    for i in range(8):
        slot_start = start + duration * i
        slot_end = start + duration * (i + 1)

        slots.append({
            "type": sequence[i % len(sequence)],
            "start": slot_start.strftime("%H:%M:%S"),
            "end": slot_end.strftime("%H:%M:%S")
        })

    return slots


def get_choghadiya(date: datetime.date, lat: float, lng: float, timezone="Asia/Kolkata"):
    """Main function to calculate day and night choghadiya"""

    tz = pytz.timezone(timezone)

    city = LocationInfo(
        name="Custom",
        region="Custom",
        timezone=timezone,
        latitude=lat,
        longitude=lng
    )

    # today's sun times
    s = sun(city.observer, date=date, tzinfo=tz)

    sunrise = s["sunrise"]
    sunset = s["sunset"]

    # next day sunrise for night calculation
    next_day = date + datetime.timedelta(days=1)
    s_next = sun(city.observer, date=next_day, tzinfo=tz)
    next_sunrise = s_next["sunrise"]

    weekday = date.weekday()  # Monday = 0
    day_sequence = DAY_SEQUENCES[weekday]

    # DAY CHOGHADIYA
    day_slots = split_into_8_parts(sunrise, sunset, day_sequence)

    # NIGHT CHOGHADIYA (continue sequence cyclically)
    night_sequence = day_sequence[1:] + [day_sequence[0]]
    night_slots = split_into_8_parts(sunset, next_sunrise, night_sequence)

    return {
        "date": str(date),
        "sunrise": sunrise.strftime("%H:%M:%S"),
        "sunset": sunset.strftime("%H:%M:%S"),
        "day_choghadiya": day_slots,
        "night_choghadiya": night_slots
    }
