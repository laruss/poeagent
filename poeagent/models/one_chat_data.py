from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .chat_messages_data import MessageData


class PoeUser(BaseModel):
    uid: int
    id: str
    creationTime: int


class Subscription(BaseModel):
    isActive: bool
    id: str
    expiresTime: int
    willCancelAtPeriodEnd: bool
    purchaseRevocationReason: None


class DefaultBot(BaseModel):
    botId: int
    id: str


class Viewer(BaseModel):
    poeUser: PoeUser
    allowImages: bool
    allowImagesForApiBots: bool
    enableImageViewer: bool
    enableMessageCitation: bool
    enableMath: bool
    promptBotImageDomainWhitelist: List[str]
    hasActiveSubscription: bool
    isEligibleForWebSubscriptions: bool
    isEligibleToPurchaseOnAnyPlatform: bool
    subscription: Subscription
    useNewLimitSystem: bool
    uid: int
    enableResendButton: bool
    useBotRecencyOrder: bool
    retryButtonEnabled: bool
    poeMessageDropdownImageOptions: bool
    shouldShowCitation: bool
    enableImageAttachmentsForBots: bool
    showTruncationWarning: bool
    decoupleBotHandleAndName: bool
    enableBotMetadata: bool
    shouldSeeWebSubscriptionAnnouncement: bool
    shouldSeeAndroidSubscriptionAnnouncement: bool
    shouldSeeResponseSpeedUpsell: bool
    showConversationStarters: bool
    defaultBot: DefaultBot
    useShareButtonRedesign: bool
    improvePrivacyConfidence: bool
    id: str


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
    totalBalance: Optional[int] = None
    freeLimit: Optional[int] = None
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
    localName: Optional[str] = None
    url: Optional[str] = None


class DefaultBotObject(BaseModel):
    deletionState: str
    viewerIsCreator: bool
    isSystemBot: bool
    isPrivateBot: bool
    viewerIsFollower: bool
    followerCount: int
    id: str
    botId: int
    shouldHide: bool
    shareLink: str
    isDown: bool
    model: str
    nickname: str
    uploadFileSizeLimit: int
    allowsImageAttachments: bool
    limitedAccessType: str
    messageLimit: MessageLimit
    messageUsageLimit: MessageUsageLimit
    displayName: str
    isOfficialBot: bool
    canUserAccessBot: bool
    isApiBot: bool
    supportsFileUpload: bool
    baseModelDisplayName: str
    allowsClearContext: bool
    introduction: str
    conversationStarters: List[str]
    handle: str
    monthlyActiveUsers: Optional[int] = None
    creator: Creator
    image: Image
    field__isNode: str = Field(..., alias='__isNode')
    description: str
    poweredBy: str
    serverBotDependenciesLimitsString: None
    messageTimeoutSecs: int
    isLimitedAccess: bool
    shouldHideLimitedAccessTag: bool
    mayHaveSuggestedReplies: bool
    supportsResend: bool
    hasWelcomeTopics: bool
    hasMarkdownRendering: bool


class LastMessage(BaseModel):
    text: str
    id: str


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


class ChatOfCode(BaseModel):
    isDeleted: bool
    title: str
    defaultBotObject: DefaultBotObject
    id: str
    chatId: int
    lastMessage: LastMessage
    field__isNode: str = Field(..., alias='__isNode')
    messagesConnection: MessagesConnection


class Data(BaseModel):
    viewer: Viewer
    chatOfCode: ChatOfCode


class Extensions(BaseModel):
    is_final: bool


class OneChatDataResponse(BaseModel):
    data: Data
    extensions: Extensions
