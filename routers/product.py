from fastapi import APIRouter, status, HTTPException
from database import Session, ENGINE
from models import User, Product
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import ProductListModel, ProductModel
from werkzeug.security import generate_password_hash, check_password_hash

session = Session(bind=ENGINE)

router = APIRouter()

@router.get("/")
async def product_list():
    products = session.query(Product).all()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        for product in products
    ]
    return jsonable_encoder(context)

@router.post("/")
async def create_products(product: ProductListModel):
    db_product = session.query(Product).filter(Product.name == product.name).first()
    if db_product is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product already excist")
    new_product = Product(
        name=product.name,
        price=product.price
    )
    session.add(new_product)
    session.commit()
    return new_product

@router.get('/{id}')
async def product_detail(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product is not None:
        context = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        return jsonable_encoder(context)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday product topilmadi")

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        session.delete(product)
        session.commit()
        data = {
            "code": 200,
            "message": f"Deleted with {id} product",
        }
        return jsonable_encoder(data)

    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday product yo'q")

@router.put('/{id}')
async def update_product(id: int, data: ProductModel):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Update product"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bunday product yo'q")