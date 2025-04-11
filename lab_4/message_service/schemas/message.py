from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, StrictStr


class MessageText(BaseModel):
    text: StrictStr = Field(min_length=1)


class Message(MessageText):
    chat_id: UUID
    sender: StrictStr = Field(min_length=1)
    sending_time: datetime


class MessageResponse(Message):
    message_id: StrictStr


class TextSearching(MessageText):
    chat_id: Optional[UUID] = None
