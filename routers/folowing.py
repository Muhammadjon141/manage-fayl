from docutils.nodes import status
from fastapi import APIRouter
from models import Follow
from database import Session, ENGINE
from schemas import FollowerModel, FollowCreateModel
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page, add_pagination, paginate

session = Session(bind=ENGINE)

router = APIRouter()

@router.get("/")
async def main_page_follow():
    return {"message": "Followerlar va Followinglar bosh qismiga xush kelibsiz!"}


@router.get("/follows", response_model=Page[dict])
async def all_follows():
    follows = session.query(Follow).all()
    return paginate(follows)


add_pagination(router_follow)


@router.post("/to_follow")
async def follow_user(follow: FollowCreateModel):
    check = session(Follow).filter(Follow.id == follow.id).first()
    if check is not None:
        session.delete(follow)
        session.commit()
        return {"message": "Follow remowed succesfully!"}
    new_follow = Follow(
        follower_id=follow.follower_id,
        following_id=follow.following_id,
    )
    session.add(new_follow)
    session.commit()
    return HTTPException(status_code=201, detail="Followed succesfully!")