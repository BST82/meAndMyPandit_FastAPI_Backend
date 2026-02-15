from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId

from configrations import festival_collection
from models.festival_model import festival_helper
from schemas.festival_schema import FestivalCreate, FestivalUpdate

router = APIRouter(prefix="/festival", tags=["Festival"])


# =========================
# CREATE FESTIVAL (Admin)
# =========================
@router.post("/")
async def create_festival(festival: FestivalCreate):
    festival_dict = festival.model_dump()

    result = await festival_collection.insert_one(festival_dict)

    new_festival = await festival_collection.find_one(
        {"_id": result.inserted_id}
    )

    return {
        "message": "Festival created successfully",
        "data": festival_helper(new_festival)
    }


# =========================
# GET ALL FESTIVALS
# =========================
@router.get("/")
async def get_all_festivals():
    festivals = []
    async for festival in festival_collection.find():
        festivals.append(festival_helper(festival))

    return {
        "total": len(festivals),
        "data": festivals
    }


# =========================
# GET CURRENT MONTH FESTIVALS
# =========================
@router.get("/current-month")
async def get_current_month_festivals():
    today = datetime.now()

    month = today.month
    year = today.year

    festivals = []
    query = {"month": month, "year": year}

    async for festival in festival_collection.find(query):
        festivals.append(festival_helper(festival))

    return {
        "month": month,
        "year": year,
        "total": len(festivals),
        "data": festivals
    }


# =========================
# UPDATE FESTIVAL
# =========================
@router.put("/{festival_id}")
async def update_festival(festival_id: str, festival: FestivalUpdate):

    if not ObjectId.is_valid(festival_id):
        raise HTTPException(status_code=400, detail="Invalid festival ID")

    update_data = {
        k: v for k, v in festival.model_dump().items() if v is not None
    }

    result = await festival_collection.update_one(
        {"_id": ObjectId(festival_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Festival not found")

    updated = await festival_collection.find_one(
        {"_id": ObjectId(festival_id)}
    )

    return {
        "message": "Festival updated",
        "data": festival_helper(updated)
    }


# =========================
# DELETE FESTIVAL
# =========================
@router.delete("/{festival_id}")
async def delete_festival(festival_id: str):

    if not ObjectId.is_valid(festival_id):
        raise HTTPException(status_code=400, detail="Invalid festival ID")

    result = await festival_collection.delete_one(
        {"_id": ObjectId(festival_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Festival not found")

    return {"message": "Festival deleted successfully"}
