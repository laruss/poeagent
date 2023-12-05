from __future__ import annotations

from pydantic import BaseModel

from ..bot import BotWithPrompt


class ChatOfCode(BaseModel):
    defaultBotObject: BotWithPrompt
    id: str


class Viewer(BaseModel):
    decoupleBotHandleAndName: bool
    id: str
    enableBotMetadata: bool


class Data(BaseModel):
    chatOfCode: ChatOfCode
    viewer: Viewer


class Extensions(BaseModel):
    is_final: bool


class ResponseByChatCode(BaseModel):
    data: Data
    extensions: Extensions
