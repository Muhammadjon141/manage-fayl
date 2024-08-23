from fastapi import APIRouter

router = APIRouter()

users = [{"message":"users list"},
        {"message":"1-Xamidov Muhammadjon"}]

@router.get("/")
def get_users():
    return users

@router.get("/login")
def get_users():
    return users

@router.get("/register")
def get_users():
    return users
    
@router.get("/password_reset")
def get_users():
    return users

@router.get("/password_confermation")
def get_users():
    return users

@router.post("/")
def create_user(user: dict):
    users.append(user)
    return users
