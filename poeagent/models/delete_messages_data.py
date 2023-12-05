from __future__ import annotations

from typing import List

from pydantic import BaseModel


class MessagesDelete(BaseModel):
    edgeIds: List[str]


class Data(BaseModel):
    messagesDelete: MessagesDelete


class Extensions(BaseModel):
    is_final: bool


class DeleteMessagesResponse(BaseModel):
    data: Data
    extensions: Extensions
