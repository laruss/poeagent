from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .common import Node, Image


class CreatedBot(Node):
    id: str
    displayName: str
    isLimitedAccess: bool
    shouldHideLimitedAccessTag: bool
    deletionState: str
    image: Optional[Image]
    handle: str
    canUserAccessBot: bool


class PoeBotCreate(BaseModel):
    status: str
    statusMessage: str
    bot: CreatedBot


class Data(BaseModel):
    poeBotCreate: PoeBotCreate


class Extensions(BaseModel):
    is_final: bool


class CreateBotResponse(BaseModel):
    data: Data
    extensions: Extensions
