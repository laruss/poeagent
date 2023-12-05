from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .chats_history_data import Chats


class Bot(BaseModel):
    displayName: str
    id: str
    botId: int


class Data(BaseModel):
    filteredChats: Chats
    bot: Bot


class Extensions(BaseModel):
    is_final: bool


class ChatHistoryFilteredResponse(BaseModel):
    data: Data
    extensions: Extensions
