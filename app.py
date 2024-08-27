from fastapi import FastAPI
from routers import auth, order, product

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags="auth"),
app.include_router(order.router, prefix="/order", tags="order"),
app.include_router(product.router, prefix="/product", tags="product"),

@app.get("/")
async def root():
    return {"message":"Home Page"}