from fastapi import APIRouter, Query, HTTPException
import datetime
from services.choghadiya_service import get_choghadiya

router = APIRouter(prefix="/choghadiya", tags=["Choghadiya"])

@router.get("/")
def fetch_choghadiya(
    date: str = Query(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
):
    try:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(400, "Invalid date format. Use YYYY-MM-DD")

    return get_choghadiya(parsed_date, latitude, longitude)
