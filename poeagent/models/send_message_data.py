from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class MessageData(BaseModel):
    messageId: int
    creationTime: int
    id: str
    text: str
    author: str
    state: str
    contentType: str
    sourceType: str
    attachmentTruncationState: str
    attachments: List
    vote: None
    suggestedReplies: List
    clientNonce: str
    hasCitations: bool
    field__isNode: str = Field(..., alias='__isNode')
    textLengthOnCancellation: None


class Message(BaseModel):
    id: str
    node: MessageData
    cursor: str


class Image(BaseModel):
    field__typename: str = Field(..., alias='__typename')
    url: str


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


class DefaultBotObject(BaseModel):
    id: str
    nickname: str
    botId: int
    hasMarkdownRendering: bool
    displayName: str
    deletionState: str
    image: Image
    viewerIsCreator: bool
    isSystemBot: bool
    isPrivateBot: bool
    viewerIsFollower: bool
    followerCount: int
    shouldHide: bool
    shareLink: str
    isDown: bool
    model: str
    uploadFileSizeLimit: int
    allowsImageAttachments: bool
    limitedAccessType: str
    messageLimit: MessageLimit
    messageUsageLimit: MessageUsageLimit
    isOfficialBot: bool
    canUserAccessBot: bool
    isApiBot: bool
    supportsFileUpload: bool
    baseModelDisplayName: str
    allowsClearContext: bool
    introduction: str
    conversationStarters: List[str]
    handle: str
    monthlyActiveUsers: int
    creator: Creator
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


class LastMessage(BaseModel):
    text: str
    id: str


class Node(BaseModel):
    messageId: int
    state: str
    text: str
    author: str
    creationTime: int
    contentType: str
    attachmentTruncationState: str
    vote: None
    suggestedReplies: List
    field__isNode: str = Field(..., alias='__isNode')
    field__typename: str = Field(..., alias='__typename')
    id: str
    textLengthOnCancellation: None
    sourceType: str
    attachments: List
    clientNonce: None
    hasCitations: bool


class Edge(BaseModel):
    node: Node
    cursor: str
    id: str


class PageInfo(BaseModel):
    hasPreviousPage: bool
    startCursor: str


class MessagesConnection(BaseModel):
    edges: List[Edge]
    pageInfo: PageInfo
    id: str


class Chat(BaseModel):
    id: str
    chatId: int
    chatCode: str
    title: Optional[str] = None
    defaultBotObject: DefaultBotObject
    lastInteractionTime: int
    lastMessage: LastMessage
    field__isNode: str = Field(..., alias='__isNode')
    isDeleted: bool
    messagesConnection: MessagesConnection


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


class MessageEdgeCreate(BaseModel):
    message: Message
    status: str
    statusMessage: str
    failedUrls: List
    chat: Chat
    viewer: Viewer


class Data(BaseModel):
    messageEdgeCreate: MessageEdgeCreate


class Extensions(BaseModel):
    is_final: bool


class SendMessageResponse(BaseModel):
    data: Data
    extensions: Extensions
