from fastapi import APIRouter
from app.model import createURL
from app.utils import generate_short_code
router= APIRouter()

@router.post("/shorten",tags=["url"])
async def Main_url(data:createURL):

    shortcode = generate_short_code()
    
    return {
        "original_url": data.mainurl,
        "new_url":shortcode
    }


    


