from urllib.request import Request
from fastapi import APIRouter, Depends
from models import Post, User
from database import Session, ENGINE
from schemas import CreatePostModel, PostModel
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Page, add_pagination, paginate

session = Session(bind=ENGINE)
router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Post Sahifasiga xush kelibsiz!!"}


@router.get("/posts", response_model=list[PostModel])
async def posts(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    posts = session.query(Post).filter(Post.user_id == user_id).all()
    return posts


@router.post("/posts")
async def create_post(post: CreatePostModel):
    check_post_id = session(Post).filter(Post.id == post.id).first()
    if check_post_id is not None:
        return HTTPException(status_code=400, detail="Post already exists")
    new_post = Post(
        user_id=post.user_id,
        image_url=post.image_url,
        caption=post.caption,
    )

    session.add(new_post)
    session.commit()
    return HTTPException(status_code=201, detail="Post created successfully!")


@router.post("/posts")
async def create_post(post: CreatePostModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    new_post = Post(
        user_id=user_id,
        image_url=post.image_url,
        caption=post.caption,
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.delete("/posts/{id}")
async def delete_post(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    post = session.query(Post).filter(Post.id == id, Post.user_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()
    return {"detail": "Post deleted successfully"}


@router.put("/posts", response_model=Page[dict])
async def posts():
    data = session.query(Post).all()
    return paginate(data)

add_pagination(router_post)