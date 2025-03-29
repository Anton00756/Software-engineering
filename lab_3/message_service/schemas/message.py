from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, StrictStr


class MessageResponse(BaseModel):
    sender: StrictStr = Field(min_length=1)
    sending_time: datetime
    text: StrictStr = Field(min_length=1)


class Message(MessageResponse):
    chat_id: UUID
