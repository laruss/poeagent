from __future__ import annotations

from typing import List, Optional, Union, Any

from pydantic import BaseModel, Field


class MessageLimit(BaseModel):
    canSend: bool
    shouldShowSubscriptionRationale: bool
    dailyLimit: None
    id: str
    numMessagesRemaining: None
    shouldShowRemainingMessageCount: bool


class MessageUsageLimit(BaseModel):
    shouldPromptSubscription: bool
    shouldShowLimitInfoBanner: bool
    id: str
    balanceTooltipText: None
    canSendMessage: bool
    totalBalance: int
    freeLimit: int
    limitType: str


class Creator(BaseModel):
    isDeleted: bool
    profilePhotoUrl: str
    fullName: str
    nullableHandle: str
    field__isNode: str = Field(..., alias='__isNode')
    id: str


class Image(BaseModel):
    field__typename: str = Field(..., alias='__typename')
    url: str


class DefaultBotObject(BaseModel):
    botId: int
    model: str
    nickname: str
    uploadFileSizeLimit: int
    allowsImageAttachments: bool
    limitedAccessType: str
    messageLimit: MessageLimit
    messageUsageLimit: MessageUsageLimit
    id: str
    isSystemBot: bool
    displayName: str
    isOfficialBot: bool
    deletionState: str
    canUserAccessBot: bool
    isApiBot: bool
    isDown: bool
    supportsFileUpload: bool
    baseModelDisplayName: str
    allowsClearContext: bool
    introduction: str
    conversationStarters: List[str]
    handle: str
    followerCount: int
    monthlyActiveUsers: int
    creator: Creator
    image: Image
    field__isNode: str = Field(..., alias='__isNode')
    description: str
    poweredBy: str
    serverBotDependenciesLimitsString: None
    messageTimeoutSecs: int
    isPrivateBot: bool
    isLimitedAccess: bool
    shouldHideLimitedAccessTag: bool
    mayHaveSuggestedReplies: bool
    supportsResend: bool
    hasWelcomeTopics: bool
    hasMarkdownRendering: bool


class LastMessage(BaseModel):
    text: str
    id: str


class MessageData(BaseModel):
    messageId: int
    state: str
    text: str
    author: str
    creationTime: int
    contentType: str
    attachmentTruncationState: str
    vote: Any = None
    suggestedReplies: List
    field__isNode: str = Field(..., alias='__isNode')
    field__typename: Optional[str] = Field(None, alias='__typename')
    id: str
    textLengthOnCancellation: Union[None, int, str] = None
    sourceType: str
    attachments: List
    clientNonce: Optional[str] = None
    hasCitations: bool


class Edge(BaseModel):
    node: MessageData
    cursor: str
    id: str


class PageInfo(BaseModel):
    hasPreviousPage: bool
    startCursor: str


class MessagesConnection(BaseModel):
    edges: List[Edge]
    pageInfo: PageInfo
    id: str


class Node(BaseModel):
    field__typename: str = Field(..., alias='__typename')
    id: str
    chatId: int
    defaultBotObject: DefaultBotObject
    lastMessage: LastMessage
    field__isNode: str = Field(..., alias='__isNode')
    messagesConnection: MessagesConnection


class Data(BaseModel):
    node: Node


class Extensions(BaseModel):
    is_final: bool


class ChatMessagesResponse(BaseModel):
    data: Data
    extensions: Extensions
