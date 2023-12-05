from __future__ import annotations

from pydantic import BaseModel

from ..bot import BotWithPrompt


class Viewer(BaseModel):
    decoupleBotHandleAndName: bool
    id: str
    enableBotMetadata: bool


class Data(BaseModel):
    botById: BotWithPrompt
    viewer: Viewer


class Extensions(BaseModel):
    is_final: bool


class ResponseByBotId(BaseModel):
    data: Data
    extensions: Extensions
