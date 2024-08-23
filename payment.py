from fastapi import APIRouter

router = APIRouter()

payments = [{"message":"payments list"}]

@router.get("/")
def get_payments():
    return payments
    
@router.post("/")
def create_payment(payment: dict):
    payments.append(payment)
    return payments
