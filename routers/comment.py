from fastapi import APIRouter, status, Depends
from models import Comment, Post
from database import Session, ENGINE
from schemas import CommentCreateModel, CommentModel
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Page, add_pagination, paginate

session = Session(bind=ENGINE)
router = APIRouter()
@router.get("/")
async def main():
    return {"message": "Comments Asosiy sahifasiga xush kelibsiz!!"}

@router.get("/comments", response_model=Page[dict])
async def get_comments():
    comments = session.query(CommentModel).all()
    return paginate(comments)
add_pagination(router_comment)

@router.post("/comment/{post_id}")
async def comment(post_id: int, comment: CommentCreateModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        user_id=user_id,
        post_id=post_id,
        comment_text=comment.comment_text,
    )
    session.add(new_comment)
    session.commit()
    return {"detail": "Comment added"}


@router.put("/comments/{id}")
async def update_comment(id: int, comment: CommentModel):
    check_id = session(Comment).filter(Comment.id == comment.id).first()
    if check_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    check_id.comment_text = comment.comment_text
    session.commit()
    session.refresh(check_id)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Comment updated successfully")


@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int):
    comment = session.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted successfully"}