from uuid import UUID

from fastapi import APIRouter, Response
from schemas.message import Message, MessageResponse

router = APIRouter()


messages = {}


@router.post('/send', summary='Send message', response_class=Response)
async def send_message(message: Message):
    messages.setdefault(message.chat_id, []).append(message)
    return Response(status_code=200)


@router.get('/history', summary='Get chat history', response_model=list[MessageResponse])
async def get_chat_history(chat_id: UUID):
    return messages.get(chat_id, [])
