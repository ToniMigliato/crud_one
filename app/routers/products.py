from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import database, models, schemas, oauth2

router = APIRouter(
    prefix='/products',
    tags=['Products'],
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)
async def create_product(product: schemas.ProductCreate, db: Session=Depends(database.get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_product = models.Products(user_id_fk=current_user.user_id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ProductResponse])
async def get_all_products(db: Session=Depends(database.get_db),
                           current_user: int=Depends(oauth2.get_current_user),
                           limit: int=10, skip: int=0, search: Optional[str]=''):
    products = db.query(models.Products).filter(models.Products.product_name.contains(search)).limit(limit).offset(skip).all()
    return products

@router.put('/{id}', response_model=schemas.ProductResponse)
async def product_update(id: int, updated_product: schemas.ProductCreate,
                         current_user: int=Depends(oauth2.get_current_user),
                         db: Session=Depends(database.get_db)):
    product_query = db.query(models.Products).filter(models.Products.product_id==id)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product id {id} does not exist.')
    if product.user_id_fk != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='you are not allowed to make updates on this product.')
    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()
    return product

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def product_delete(id: int, current_user: int=Depends(oauth2.get_current_user),
                         db: Session=Depends(database.get_db)):
    product_query = db.query(models.Products).filter(models.Products.product_id==id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product id {id} not found in database.')
    if product.user_id_fk != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not allowed to delete this product.')
    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)