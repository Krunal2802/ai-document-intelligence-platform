from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def check():
    return {"message":"user router is working!!!"}