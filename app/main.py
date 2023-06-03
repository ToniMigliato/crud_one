from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, users, products, receipts

# models.Base.metadat a.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(receipts.router)

@app.get('/')
async def root():
    return {'message': 'This should be a CRUD operations system!!'}