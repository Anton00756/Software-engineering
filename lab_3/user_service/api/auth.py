from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import AuthResponse
from utils import PasswordEngine, TokenEngine

from .user import users

router = APIRouter()


@router.post(
    '/token',
    summary='Authenticate in system',
    responses={401: {'description': 'Incorrect username or password'}},
    response_model=AuthResponse,
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    password_check = False
    if form_data.username in users:
        password_check = PasswordEngine.verify_password(form_data.password, users[form_data.username].password)
    if password_check:
        access_token = TokenEngine.create_access_token(form_data.username)
        return AuthResponse(access_token=access_token, token_type='bearer')
    raise HTTPException(
        status_code=401,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )
