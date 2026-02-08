from fastapi import APIRouter, HTTPException
from schemas.home_schema import HomeCreate
from configrations import db
from bson import ObjectId

router = APIRouter(prefix="/home", tags=["Home"])

@router.post("/")
async def create_home_content(payload: HomeCreate):
    document = {
        "mantras": payload.mantras,
        "data": payload.data,
        "isActive": True
    }

    await db.homecontent.insert_one(document)
    return { "message": "Home content created successfully" }


@router.get("/")
async def get_home_content():
    content = await db.homecontent.find_one(
        { "isActive": True },
        { "_id": 0 }
    )

    if not content:
        raise HTTPException(status_code=404, detail="Home content not found")

    return content


@router.put("/{content_id}")
async def update_home_content(content_id: str, payload: HomeCreate):
    result = await db.homecontent.update_one(
        { "_id": ObjectId(content_id) },
        {
            "$set": {
                "mantras": payload.mantras,
                "data": payload.data
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Home content not found")

    return { "message": "Home content updated successfully" }


@router.delete("/{content_id}")
async def delete_home_content(content_id: str):
    result = await db.homecontent.update_one(
        { "_id": ObjectId(content_id) },
        { "$set": { "isActive": False } }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Home content not found")

    return { "message": "Home content deleted successfully" }
