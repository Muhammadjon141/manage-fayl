from fastapi import APIRouter, status
from database import Session, ENGINE
from models import User, Product
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from schemas import ProductListModel

session = Session(bind=ENGINE)

router = APIRouter()

@router.get("/")
async def products():
    return {"message":"products"}

@router.post("/")
async def create_products(product: ProductListModel):
    db_product = session.query(Product).filter(Product.name == product.name).first()
    if db_product is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product already excist")
    new_product = User(
        name=product.name,
        price=product.price
    )
    session.add(new_product)
    session.commit()
    return new_product