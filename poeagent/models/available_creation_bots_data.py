from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class BotsAllowedForUserCreationItem(BaseModel):
    displayName: str
    model: str
    allowsUserCreation: bool
    baseModelDisplayName: str
    limitedAccessType: str
    maxTokensForPrompt: int
    maxTokensForIntroduction: Optional[int]
    modelDefaultTemperature: Optional[float]
    modelMaxTemperature: float
    botId: int
    showAdvancedFieldsAsBaseBot: bool
    id: str


class Viewer(BaseModel):
    enableBotEditReminder: bool
    botsAllowedForUserCreation: List[BotsAllowedForUserCreationItem]
    enablePromptBotsPrivacySetting: bool
    enablePromptBotCustomTemperature: bool
    decoupleBotHandleAndName: bool
    isEnrolledInRevshare: bool
    shouldSeeRevshareEntryPoints: bool
    showKnowledgeBaseSection: bool
    canEditMessagePrice: bool
    knowledgeBaseSizeLimit: int
    id: str


class Data(BaseModel):
    randomizedAvailableBotHandle: str
    viewer: Viewer
    message: None


class Extensions(BaseModel):
    is_final: bool


class AvailableCreationBotsResponse(BaseModel):
    data: Data
    extensions: Extensions
