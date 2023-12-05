from __future__ import annotations

from pydantic import BaseModel, Field


class Creator(BaseModel):
    isDeleted: bool
    profilePhotoUrl: str
    fullName: str
    nullableHandle: str
    field__isNode: str = Field(..., alias='__isNode')
    id: str


class DeletedBotData(BaseModel):
    botId: int
    handle: str
    displayName: str
    followerCount: int
    monthlyActiveUsers: None
    isSystemBot: bool
    creator: Creator
    deletionState: str
    image: None
    field__isNode: str = Field(..., alias='__isNode')
    id: str
    description: str
    poweredBy: str
    limitedAccessType: str
    viewerIsFollower: bool
    shouldHide: bool
    shareLink: str
    promptPlaintext: str
    viewerIsCreator: bool
    canUserAccessBot: bool


class PoeBotDelete(BaseModel):
    status: str
    bot: DeletedBotData


class Data(BaseModel):
    poeBotDelete: PoeBotDelete


class Extensions(BaseModel):
    is_final: bool


class DeleteBotResponse(BaseModel):
    data: Data
    extensions: Extensions
