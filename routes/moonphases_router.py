from fastapi import APIRouter, HTTPException
from configrations import db
import requests
from datetime import datetime

router = APIRouter(prefix="/moon", tags=["Moon Panchang"])

WEATHER_API_KEY = "635a64d5fb094a7ba6b133856261402"


@router.get("/phase")
async def get_moon_phase(lat: float, lng: float):
    try:
        # Round location
        lat = round(lat, 2)
        lng = round(lng, 2)

        print("LAT:", lat, "LNG:", lng)  # debug

        # STEP 1 — Check DB
        cached = await db.moon_phases.find_one(
            {"lat": lat, "lng": lng},
            {"_id": 0}
        )

        if cached:
            print("Returning from DB")
            return {"source": "database", **cached}

        print("Calling Weather API...")

        # STEP 2 — Weather API
        url = f"https://api.weatherapi.com/v1/astronomy.json?key={WEATHER_API_KEY}&q={lat},{lng}"

        response = requests.get(url, timeout=5)

        print("Weather Status:", response.status_code)

        data = response.json()
        print("Weather Response:", data)

        # Handle API error
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=data)

        # Validate keys
        if "astronomy" not in data:
            raise HTTPException(status_code=400, detail="No astronomy data found")

        result = {
            "lat": lat,
            "lng": lng,
            "location": {
                "city": data["location"]["name"],
                "region": data["location"]["region"],
                "country": data["location"]["country"]
            },
            "moon_data": {
                "moon_phase": data["astronomy"]["astro"]["moon_phase"],
                "moon_illumination": data["astronomy"]["astro"]["moon_illumination"],
                "moonrise": data["astronomy"]["astro"]["moonrise"],
                "moonset": data["astronomy"]["astro"]["moonset"]
            },
            "createdAt": datetime.utcnow()
        }

        # STEP 3 — Save to DB
        await db.moon_phases.insert_one(result)

        print("Saved to DB")

        return {"source": "weather_api", **result}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Weather API timeout")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Weather API connection failed")

    except Exception as e:
        print("ERROR:", str(e))  # see error in terminal
        raise HTTPException(status_code=500, detail=str(e))
