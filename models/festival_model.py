def festival_helper(festival) -> dict:
    return {
        "id": str(festival["_id"]),
        "name": festival["name"],
        "date": festival["date"],
        "month": festival["month"],
        "year": festival["year"],
        "description": festival.get("description"),
    }
