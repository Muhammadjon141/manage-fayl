from fastapi import FastAPI
import auth, cargo, payment, store

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(payment.router, prefix="/payment", tags=["Payment"])
app.include_router(cargo.router, prefix="/cargo", tags=["Cargo"])
app.include_router(store.router, prefix="/store", tags=["Store"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Learning Platform API"}
