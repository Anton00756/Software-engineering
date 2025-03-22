import re

from fastapi import APIRouter, Depends, HTTPException, Response
from schemas.auth import AuthResponse
from schemas.user import SearchUser, UserBase, UserCreate
from utils import PasswordEngine, TokenEngine

from .token_utils import get_current_user

router = APIRouter()


users = {
    'admin': UserCreate(login='admin', password=PasswordEngine.hash_password('secret'), name='admin', surname='admin'),
}


@router.post(
    '/register',
    summary='Register new user',
    response_model=AuthResponse,
    responses={409: {'description': 'User already exists'}},
)
async def register_user(user: UserCreate):
    if user.login in users:
        raise HTTPException(status_code=409, detail='User already exists')
    user.password = PasswordEngine.hash_password(user.password)
    users[user.login] = user
    access_token = TokenEngine.create_access_token(user.login)
    return AuthResponse(access_token=access_token, token_type='bearer')


@router.get(
    '/info',
    summary='Get information about current user',
    response_model=UserBase,
    responses={401: {}, 404: {'description': 'User wasn`t found'}},
)
async def get_user_info(current_user: str = Depends(get_current_user)):
    if current_user not in users:
        raise HTTPException(status_code=404, detail='User wasn`t found')
    return users[current_user]


@router.get('/list', summary='Get list of users', response_model=list[UserBase], responses={401: {}})
async def get_user_list(current_user: str = Depends(get_current_user)):
    return list(users.values())


@router.delete(
    '/delete',
    summary='Delete current user',
    response_class=Response,
    responses={401: {}, 404: {'description': 'User wasn`t found'}},
)
async def delete_user(current_user: str = Depends(get_current_user)):
    if current_user not in users:
        return HTTPException(status_code=404, detail='User wasn`t found')
    users.pop(current_user)
    return Response(status_code=200)


@router.post('/search', summary='Search user', response_model=list[UserBase])
async def search_user(searching: SearchUser):
    results = []
    for user in users.values():
        user_info = user.model_dump()
        for field in searching.fields:
            if re.match(searching.value, user_info.get(field, '')):
                results.append(user)
                break
    return results
