from fastapi import APIRouter, status
from database import Session, ENGINE
from models import User, Order, Product
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import OrderListModel
from werkzeug.security import generate_password_hash, check_password_hash

session = Session(bind=ENGINE)

router = APIRouter()

@router.get("/")
async def order_list():
    orders = session.query(Order).all()
    context = [
        {
            "id": order.id,
            "order_status": order.order_status,
            "user_id": order.user_id,
            "product_id": order.product_id
        }
        for order in orders
    ]
    return jsonable_encoder(context)

@router.post("/")
async def create_order(order: OrderListModel):
    db_order = session.query(Order).filter(Order.id == order.id).first()
    if db_order is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This order already excist")
    db_user = session.query(User).filter(User.id == order.user_id).first()
    if db_user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not found")
    db_product = session.query(Product).filter(Product.id == order.product_id).first()
    if db_product is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This product not found")
    
    new_order = Order(
        id = order.id,
        quantity=order.quantity,
        order_status=order.order_status,
        user_id=order.user_id,
        product_id=order.product_id
    )
    session.add(new_order)
    session.commit()
    return order

@router.get('/{id}')
async def order_detail(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if order is not None:
        context = {
            "id": order.id,
            "quantity": order.quantity,
            "order_status": order.order_status,
            "user_id": order.user_id,
            "product_id": order.product_id
        }
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday order topilmadi")

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if order:
        session.delete(order)
        session.commit()
        data = {
            "code": 200,
            "message": f"Deleted with {id} order",
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday order yo'q")

@router.put('/{id}')
async def update_order(id: int, data: OrderListModel):
    order = session.query(Order).filter(Order.id == id).first()
    if order:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(order, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Update order"
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bunday product yo'q")