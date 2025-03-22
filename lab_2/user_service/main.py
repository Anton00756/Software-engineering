import logging

import uvicorn
from api import auth_router, user_router
from fastapi import FastAPI

app = FastAPI(title='T-Mess', description='User service', version='1.0', docs_url='/api/docs')

app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(user_router, prefix='/user', tags=['Users'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', log_level=logging.DEBUG, reload=True)
