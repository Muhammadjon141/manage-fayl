from fastapi import APIRouter

router = APIRouter()

stories = [{"message":"stories"}]



@router.get("/")
def get_stories():
    return stories
    
@router.post("/")
def create_story(story: dict):
    stories.append(story)
    return stories
