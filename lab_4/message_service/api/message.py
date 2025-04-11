from typing import Optional
from uuid import UUID

from bson import ObjectId, errors
from fastapi import APIRouter, HTTPException, Response
from pymongo import mongo_client
from schemas.message import Message, MessageResponse, MessageText

router = APIRouter()

client = mongo_client.MongoClient(host='mongo', port=27017, uuidRepresentation='standard')
messages = client['messenger']['messages']


def convert_message(item):
    item['message_id'] = str(item['_id'])
    return item


@router.post('/send', summary='Send message', response_model=MessageResponse)
async def send_message(message: Message):
    result = messages.insert_one(message.model_dump())
    return MessageResponse(**message.model_dump(), message_id=str(result.inserted_id))


@router.put(
    '/update/{message_id}',
    summary='Send message',
    response_model=MessageResponse,
    responses={400: {'description': 'Invalid message_id format'}},
)
async def update_message(message_id: str, message_text: MessageText):
    try:
        object_id = ObjectId(message_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='Invalid message_id format')
    messages.update_one({'_id': object_id}, {'$set': {'text': message_text.text}})
    return Response(status_code=200)


@router.delete(
    '/delete/{message_id}',
    summary='Send message',
    response_class=Response,
    responses={400: {'description': 'Invalid message_id format'}},
)
async def delete_message(message_id: str):
    try:
        object_id = ObjectId(message_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='Invalid message_id format')
    messages.delete_one({'_id': object_id})
    return Response(status_code=200)


@router.get('/history', summary='Get chat history', response_model=list[MessageResponse])
async def get_chat_history(chat_id: Optional[UUID] = None):
    if chat_id is None:
        return list(map(convert_message, messages.find()))
    return list(map(convert_message, messages.find({'chat_id': {'$eq': chat_id}})))


@router.get('/find', summary='Find text in message', response_model=list[MessageResponse])
async def find_text_in_message(text: str, chat_id: Optional[UUID] = None):
    request = {'$text': {'$search': f'"{text}"'}}
    if chat_id is not None:
        request.update({'chat_id': {'$eq': chat_id}})
    return list(map(convert_message, messages.find(request)))
