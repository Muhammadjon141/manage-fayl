from fastapi import FastAPI
from routers import auth, posts, likes
from schemas import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth.router, prefix="/auth", tags="auth"),
app.include_router(posts.router, prefix="/posts", tags="posts"),
app.include_router(likes.router, prefix="/likes", tags="likes"),

@app.get("/")
async def root():
    return {"message":"Home Page"}