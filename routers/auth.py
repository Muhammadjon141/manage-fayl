from fastapi import APIRouter, status
from database import Session, ENGINE
from models import User, Order
from schemas import RegisterModel, LoginModel, UserOrdersListModel
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

session = Session(bind=ENGINE)

router = APIRouter()

@router.get("/")
async def auth_page(id: UserOrdersListModel):
    db_order = session.query(Order).filter(Order.user_id == id).first()
    if db_order is not None:
        return HTTPException(status_code=status.HTTP_200_OK, detail=f"{db_order}")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="orders not found")

@router.get("/login")
async def login_page():
    return {"message": "Login page"}

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_page(user: LoginModel):
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        if check_password_hash(db_username.password, user.password):
            return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Logined succesfully")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong username")        
    
@router.get("/register")
async def register_page():
    return {"message": "Register page"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return new_user

@router.get("/users")
async def get_users():
    users = session.query(User).all()
    return users