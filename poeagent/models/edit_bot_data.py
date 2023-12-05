from __future__ import annotations

from pydantic import BaseModel


class EditBotData(BaseModel):
    handle: str
    id: str


class PoeBotEdit(BaseModel):
    status: str
    statusMessage: str
    bot: EditBotData


class Data(BaseModel):
    poeBotEdit: PoeBotEdit


class Extensions(BaseModel):
    is_final: bool


class EditBotResponse(BaseModel):
    data: Data
    extensions: Extensions
