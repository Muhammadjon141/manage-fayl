from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def products():
    return {"message":"products"}