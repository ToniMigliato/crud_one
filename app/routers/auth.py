from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas, oauth2, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.user_email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials.')
    if not utils.verify(user_credentials.password, user.user_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials.')
    access_token = oauth2.create_access_token(data={'user_id': user.user_id})
    return {'access_token': access_token, 'token_type': 'bearer'}
