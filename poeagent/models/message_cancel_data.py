from __future__ import annotations

from pydantic import BaseModel


class Message(BaseModel):
    id: str
    state: str
    text: str
    textLengthOnCancellation: int


class MessageCancel(BaseModel):
    message: Message


class Data(BaseModel):
    messageCancel: MessageCancel


class Extensions(BaseModel):
    is_final: bool


class MessageCancelResponse(BaseModel):
    data: Data
    extensions: Extensions
