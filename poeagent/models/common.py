from typing import Optional

from pydantic import BaseModel, Field


class Node(BaseModel):
    field__isNode: str = Field(..., alias='__isNode')


class Creator(Node):
    isDeleted: bool
    profilePhotoUrl: str
    fullName: str
    nullableHandle: str
    id: str


class Image(BaseModel):
    field__typename: str = Field(..., alias='__typename')
    url: Optional[str] = None
    localName: Optional[str] = None


class MessageLimit(BaseModel):
    shouldShowRemainingMessageCount: bool
    numMessagesRemaining: None
    id: str
    canSend: bool
    shouldShowSubscriptionRationale: bool
    dailyLimit: None


class MessageUsageLimit(BaseModel):
    balanceTooltipText: None
    id: str
    canSendMessage: bool
    shouldPromptSubscription: bool
    shouldShowLimitInfoBanner: bool
