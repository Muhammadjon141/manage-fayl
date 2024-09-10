import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import User, Post, Likes
from schemas import UserRegister, UserLogin, UserPasswordReset, UserPostCreateSchema
from database import ENGINE, Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_


session = Session(bind=ENGINE)

router = APIRouter()

@router.get('/')
async def get_auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    return HTTPException(status_code=status.HTTP_200_OK, detail="auth page")

@router.post('/login', status_code=200)
async def login_user(user: UserLogin, Authorize: AuthJWT = Depends()):
    check_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )).first()
    if check_user is not None:
        if check_password_hash(check_user.password, user.password):
            access_lifetime = datetime.timedelta(minutes=10)
            refresh_lifetime = datetime.timedelta(days=3)
            access_token = Authorize.create_access_token(subject=check_user.username, expires_time=access_lifetime)
            refresh_token = Authorize.create_refresh_token(subject=check_user.username, expires_time=refresh_lifetime)
            token = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "token": token
            }
            return jsonable_encoder(response)
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

@router.post('/register')
async def register_user(user: UserRegister, Authorize: AuthJWT = Depends()):
    check_user = session.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
            )).first()
    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    session.query(User)
    session.add(new_user)
    session.commit()
    access_lifetime = datetime.timedelta(minutes=10)
    refresh_lifetime = datetime.timedelta(days=3)
    access_token = Authorize.create_access_token(subject=user.username, expires_time=access_lifetime)
    refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=refresh_lifetime)
    token = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    response = {
        "code": status.HTTP_200_OK,
        "success": True,
        "message": "registered succesfully",
        "token": token
    }
    return jsonable_encoder(response)

@router.get('/users')
async def get_users(Authenticate: AuthJWT = Depends()):
    try:
        Authenticate.jwt_required()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")
    user = session.query(User).filter(User.username == Authenticate.get_jwt_subject()).first()
    if user is not None:
        users = session.query(User).all()
        return jsonable_encoder(users)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, default="Invalid Token")

@router.get('/login/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        access_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(days=3)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        check_user = session.query(User).filter(User.username == current_user).first()
        if check_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        new_access_token = Authorize.create_access_token(subject=check_user.username, expires_time=access_lifetime)

        response = {
            "code": 200,
            "success": True,
            "message": "New refresh token created",
            "data": new_access_token
        }
        return jsonable_encoder(response)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
@router.get("/{username}")
async def user_profil(username: str, authenticate: AuthJWT = Depends()):
    try:
        authenticate.jwt_required()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")
    try:
        user = session.query(User).filter(User.username == username).first()
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    if user is not None:
        posts_user = session.query(Post).filter(Post.user_id == user.id).all()
        if posts_user is not None:
            posts = {
            "status": 200,
            "message": f"{user.username}ning postlari",
            "posts": [
                {
                    "image": post_user.image_path,
                    "caption": post_user.caption,
                    "review": post_user.review
                }
                for post_user in posts_user
                ]
            
            }
            for post_user in posts_user:
                post_user.review += 1
            session.add(post_user)
            session.commit()
            return jsonable_encoder(posts)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="posts not found")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

@router.post("/post/create")
async def post_create(post: UserPostCreateSchema, authenticate: AuthJWT = Depends()):
    try:
        authenticate.jwt_required()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")
    
    user_post = session.query(User).filter(User.username == authenticate.get_jwt_subject()).first()
    
    if user_post is not None:
        new_post = Post(
        user_id = user_post.id,
        image_path = post.image_path,
        caption = post.caption,
        review = post.review
        )
        posts = {
            "user":200,
            "message":f"{user_post.username}ning yaratgan postingiz",
            "posts":post
        }
        post = session.query(Post)
        session.add(new_post)
        session.commit()
        return jsonable_encoder(posts)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")