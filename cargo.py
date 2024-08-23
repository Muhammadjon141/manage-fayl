from fastapi import APIRouter

router = APIRouter()

orders = [{"message":"orders list"}]
delivery = [{"message":'delivery list'}]

@router.get("/")
def get_orders():
    return orders

@router.get("/delivery")
def get_delivery():
    return delivery

@router.get("/orders")
def get_orders():
    return orders

@router.get("/order_story")
def get_orders():
    return orders

@router.post("/order")
def create_order(order: dict):
    orders.append(order)
    return orders
