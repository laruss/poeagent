from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Image(BaseModel):
    field__typename: str = Field(..., alias='__typename')
    url: str


class DefaultBotObject(BaseModel):
    botId: int
    displayName: str
    deletionState: str
    image: Optional[Image]
    id: str


class LastMessage(BaseModel):
    text: str
    id: str


class ChatHistoryData(BaseModel):
    id: str
    chatId: int
    chatCode: str
    title: str
    lastInteractionTime: int
    defaultBotObject: DefaultBotObject
    lastMessage: LastMessage
    field__isNode: str = Field(..., alias='__isNode')
    field__typename: str = Field(..., alias='__typename')


class Edge(BaseModel):
    node: ChatHistoryData
    cursor: str
    id: str


class PageInfo(BaseModel):
    endCursor: str
    hasNextPage: bool


class Chats(BaseModel):
    edges: List[Edge]
    pageInfo: PageInfo
    id: str


class Data(BaseModel):
    chats: Chats


class Extensions(BaseModel):
    is_final: bool


class ChatsHistoryResponse(BaseModel):
    data: Data
    extensions: Extensions
