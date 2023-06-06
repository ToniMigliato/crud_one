from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import database, models, schemas, oauth2

router = APIRouter(
    prefix='/customers',
    tags=['Customers'],
)

@router.post('/', response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: schemas.CustomerCreate,
                          current_user: int=Depends(oauth2.get_current_user),
                          db: Session=Depends(database.get_db)):
    customer_query = db.query(models.Customers).filter(models.Customers.customer_email==customer.customer_email).first()
    if customer_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Customer {customer.customer_email} already exists.')
    new_customer = models.Customers(user_id_fk=current_user.user_id, **customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get('/', response_model=List[schemas.CustomerResponse], status_code=status.HTTP_200_OK)
async def get_all_customers(current_user: int=Depends(oauth2.get_current_user),
                            db: Session=Depends(database.get_db),
                            limit: int=10, skip: int=0, search: Optional[str]=''):
    customers = db.query(models.Customers).filter(models.Customers.customer_email.contains(search)).limit(limit).offset(skip).all()
    return customers

@router.get('/{id}', response_model=schemas.CustomerResponse, status_code=status.HTTP_200_OK)
async def get_customer(id: int,
                       db: Session=Depends(database.get_db),
                       current_user: int=Depends(oauth2.get_current_user)):
    customer = db.query(models.Customers).filter(models.Customers.customer_id==id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Customer id {id} not found.')
    return customer

@router.put('/{id}', response_model=schemas.CustomerResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_customer(id: int, update_customer: schemas.CustomerCreate,
                          current_user: int=Depends(oauth2.get_current_user),
                          db: Session=Depends(database.get_db)):
    customer_query = db.query(models.Customers).filter(models.Customers.customer_id==id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Customer id {id} not found.')
    customer_query.update(update_customer.dict(), synchronize_session=False)
    db.commit()
    return customer

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(id: int,
                          current_user: int=Depends(oauth2.get_current_user),
                          db: Session=Depends(database.get_db)):
    delete_customer = db.query(models.Customers).filter(models.Customers.customer_id==id)
    customer = delete_customer.first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Customer id {id} not found.')
    if customer.user_id_fk != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not authorized to perform this operation.')
    delete_customer.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)