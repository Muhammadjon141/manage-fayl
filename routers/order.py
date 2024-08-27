from fastapi import APIRouter, status
from database import Session, ENGINE
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

session = Session(bind=ENGINE)

router = APIRouter()

@router.get("/")
async def orders():
    return {"message":"orders"}