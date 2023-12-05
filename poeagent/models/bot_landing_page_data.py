from __future__ import annotations

from typing import List

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
    totalBalance: None
    freeLimit: None
    limitType: str


class Creator(BaseModel):
    isDeleted: bool
    profilePhotoUrl: str
    fullName: str
    nullableHandle: str
    field__isNode: str = Field(..., alias='__isNode')
    id: str


class LandingBotData(BaseModel):
    displayName: str
    isEligibleForLoggedOutUsage: bool
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
    monthlyActiveUsers: None
    creator: Creator
    image: None
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
    viewerIsFollower: bool
    shouldHide: bool
    shareLink: str


class PageInfo(BaseModel):
    endCursor: None
    hasNextPage: bool


class Chats(BaseModel):
    edges: List
    pageInfo: PageInfo
    id: str


class PoeUser(BaseModel):
    id: str
    uid: int
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
    isLoggedOutUsageEnabled: bool
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


class Data(BaseModel):
    bot: LandingBotData
    chats: Chats
    viewer: Viewer


class Extensions(BaseModel):
    is_final: bool


class GetBotLandingPageDataResponse(BaseModel):
    data: Data
    extensions: Extensions
