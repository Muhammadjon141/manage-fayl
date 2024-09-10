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

@router.get("/")
async def user_likes(authenticate: AuthJWT = Depends()):
    try:
        authenticate.jwt_required()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")
    
    user = session.query(User).filter(User.username == authenticate.get_jwt_subject()).first()
    if user is not None:
        like_posts = session.query(Likes).filter(Likes.user_id == user.id).all()
        posts = [{
            "status": 200,
            "message":"like bosgan postlaringiz",
            "posts": {like_post}
            }
                 for like_post in like_posts
                 ]
        return jsonable_encoder(posts)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")