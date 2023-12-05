from __future__ import annotations

from pydantic import BaseModel


class DeleteChat(BaseModel):
    deletedChatId: int


class Data(BaseModel):
    deleteChat: DeleteChat


class Extensions(BaseModel):
    is_final: bool


class DeleteChatResponse(BaseModel):
    data: Data
    extensions: Extensions
