from fastapi import APIRouter
from services.monthly_muhurat_service import get_current_month_muhurats
from datetime import datetime

router = APIRouter(prefix="/muhurats", tags=["Shubh Muhurat"])


@router.get("/current-month")
async def current_month_muhurats():
    return {
        "month": datetime.now().strftime("%B"),
        "year": datetime.now().year,
        "data": get_current_month_muhurats()
    }
