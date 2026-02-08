from fastapi import APIRouter
from schemas.footer_schema import FooterCreate
from configrations import db
from bson import ObjectId

router = APIRouter(prefix="/footer", tags=["Footer"])


@router.get("/")
async def get_footer():
    pages = await db.footerpages.find(
        { "isActive": True },
        { "_id": 0, "name": 1, "slug": 1 }
    ).to_list(None)

    return { "pages": pages }


@router.post("/")
async def create_footer(payload: FooterCreate):
    await db.footerpages.insert_one({
        "name": payload.name,
        "slug": payload.slug,
        "isActive": True
    })
    return { "message": "Footer page created" }


@router.put("/{footer_id}")
async def update_footer(footer_id: str, payload: FooterCreate):
    await db.footerpages.update_one(
        { "_id": ObjectId(footer_id) },
        { "$set": payload.dict() }
    )
    return { "message": "Footer page updated" }


@router.delete("/{footer_id}")
async def delete_footer(footer_id: str):
    await db.footerpages.delete_one({ "_id": ObjectId(footer_id) })
    return { "message": "Footer page deleted" }
