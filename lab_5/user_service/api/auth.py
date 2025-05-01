from database import get_db
from db_models import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import AuthResponse
from sqlalchemy.orm import Session
from utils import PasswordEngine, TokenEngine

router = APIRouter()


@router.post(
    '/token',
    summary='Authenticate in system',
    responses={401: {'description': 'Incorrect username or password'}},
    response_model=AuthResponse,
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    password_check = False
    existing_user = db.query(User).filter(User.login == form_data.username).first()
    print(existing_user.login)
    if existing_user:
        print(form_data.password, existing_user.password)
        print(PasswordEngine.hash_password(form_data.password))
        print(PasswordEngine.hash_password(form_data.password))
        password_check = PasswordEngine.verify_password(form_data.password, existing_user.password)
        print(password_check)
    if password_check:
        access_token = TokenEngine.create_access_token(form_data.username)
        return AuthResponse(access_token=access_token, token_type='bearer')
    raise HTTPException(
        status_code=401,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )
