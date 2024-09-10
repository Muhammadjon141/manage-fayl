import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import User, Post, Likes
from schemas import UserRegister, UserLogin, UserPasswordReset
from database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

session = Session(bind=ENGINE)

router = APIRouter()

