from fastapi import APIRouter
from schemas.header_schema import HeaderCreate
from configrations import db
from bson import ObjectId

router = APIRouter(prefix="/header", tags=["Header"])


@router.get("/")
async def get_header():
    pipeline = [
    { "$match": { "isActive": True }},

    {
        "$lookup": {
            "from": "cities",
            "localField": "_id",
            "foreignField": "headerId",
            "as": "cities"
        }
    },

    {
        "$lookup": {
            "from": "places",
            "let": { "cityIds": "$cities._id" },
            "pipeline": [
                {
                    "$match": {
                        "$expr": { "$in": ["$cityId", "$$cityIds"] }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "name": 1,
                        "slug": 1,
                        "cityId": 1
                    }
                }
            ],
            "as": "places"
        }
    },

    {
        "$addFields": {
            "cities": {
                "$map": {
                    "input": "$cities",
                    "as": "city",
                    "in": {
                        "name": "$$city.name",
                        "slug": "$$city.slug",
                        "places": {
                            "$filter": {
                                "input": "$places",
                                "as": "place",
                                "cond": {
                                    "$eq": ["$$place.cityId", "$$city._id"]
                                }
                            }
                        }
                    }
                }
            }
        }
    },

    {
        "$project": {
            "_id": 0,
            "name": 1,
            "slug": 1,
            "type": 1,
            "cities": {
                "$cond": [
                    { "$eq": ["$type", "dropdown"] },
                    "$cities",
                    "$$REMOVE"
                ]
            }
        }
    },

    # 🔥 FINAL CLEAN JSON STAGE (THIS FIXES THE ERROR)
    {
        "$project": {
            "name": 1,
            "slug": 1,
            "type": 1,
            "cities": {
                "$map": {
                    "input": "$cities",
                    "as": "city",
                    "in": {
                        "name": "$$city.name",
                        "slug": "$$city.slug",
                        "places": {
                            "$map": {
                                "input": "$$city.places",
                                "as": "place",
                                "in": {
                                    "name": "$$place.name",
                                    "slug": "$$place.slug"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
]


    result = await db.headermenu.aggregate(pipeline).to_list(None)
    return { "menu": result }


@router.post("/")
async def create_header(payload: HeaderCreate):
    header_doc = {
        "name": payload.name,
        "slug": payload.slug,
        "type": payload.type,
        "isActive": True
    }

    header_result = await db.headermenu.insert_one(header_doc)
    header_id = header_result.inserted_id

    if payload.type == "dropdown":
        for city in payload.cities:
            city_doc = {
                "headerId": header_id,
                "name": city.name,
                "slug": city.slug,
                "isActive": True
            }
            city_result = await db.cities.insert_one(city_doc)

            for place in city.places:
                await db.places.insert_one({
                    "cityId": city_result.inserted_id,
                    "name": place.name,
                    "slug": place.slug,
                    "isActive": True
                })

    return { "message": "Header created successfully" }


@router.put("/{header_id}")
async def update_header(header_id: str, payload: HeaderCreate):
    await db.headermenu.update_one(
        { "_id": ObjectId(header_id) },
        { "$set": payload.dict(exclude={"cities"}) }
    )
    return { "message": "Header updated successfully" }


@router.delete("/{header_id}")
async def delete_header(header_id: str):
    hid = ObjectId(header_id)

    cities = await db.cities.find({ "headerId": hid }).to_list(None)
    city_ids = [c["_id"] for c in cities]

    await db.places.delete_many({ "cityId": { "$in": city_ids } })
    await db.cities.delete_many({ "headerId": hid })
    await db.headermenu.delete_one({ "_id": hid })

    return { "message": "Header deleted successfully" }
