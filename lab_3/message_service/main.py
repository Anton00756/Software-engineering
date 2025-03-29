import logging

import uvicorn
from api import message_router
from fastapi import FastAPI

app = FastAPI(title='T-Mess', description='Message service', version='1.0', docs_url='/api/docs')

app.include_router(message_router, prefix='/message', tags=['Messages'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', log_level=logging.DEBUG, reload=True)
