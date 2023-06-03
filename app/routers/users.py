from typing import List
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils, oauth2

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session=Depends(database.get_db)):
    hashed_password = utils.hash(user.user_password)
    user.user_password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
async def get_all_users(db: Session=Depends(database.get_db),
                        current_user: int=Depends(oauth2.get_current_user)):
    users = db.query(models.Users).all()
    print('USERS', users[0].user_name)
    return users

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def get_user(id: int, db: Session=Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.user_id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {id} does not exist.')
    return user

@router.put('/{id}', response_model=schemas.UserResponse)
async def user_update(id: int, updated_user: schemas.UserCreate,
                      current_user: int=Depends(oauth2.get_current_user),
                      db: Session=Depends(database.get_db)):
    user_query = db.query(models.Users).filter(models.Users.user_id==id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User id {id} not found in database.')
    if user.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not allowed to update this user.')
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(id: int, currente_user: int=Depends(oauth2.get_current_user),
                      db: Session=Depends(database.get_db)):
    user_query = db.query(models.Users).filter(models.Users.user_id==id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User id {id} not found in database.')
    if user.user_id != currente_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not allowed to delete this user.')
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)