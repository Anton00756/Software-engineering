from enum import Enum

from pydantic import BaseModel, Field, StrictStr


class UserBase(BaseModel):
    login: StrictStr = Field(min_length=1)
    name: StrictStr = Field(min_length=1)
    surname: StrictStr = Field(min_length=1)


class UserCreate(UserBase):
    password: StrictStr = Field(min_length=1)


class AvaliableSearchingFields(str, Enum):
    LOGIN = 'login'
    NAME = 'name'
    SURNAME = 'surname'


class SearchUser(BaseModel):
    fields: list[AvaliableSearchingFields] = Field(list(AvaliableSearchingFields), min_length=1)
    value: StrictStr = Field(min_length=1)
