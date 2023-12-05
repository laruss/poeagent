from typing import Optional, List

from .common import Image, MessageLimit, MessageUsageLimit, Node, Creator


class BaseBot(Node):
    id: str
    botId: int
    handle: str
    displayName: str
    isSystemBot: bool
    deletionState: str
    image: Optional[Image]
    limitedAccessType: str
    canUserAccessBot: bool


class OverviewBot(BaseBot):
    isLimitedAccess: bool
    shouldHideLimitedAccessTag: bool
    isApiBot: bool
    isDown: bool
    uploadFileSizeLimit: int
    allowsImageAttachments: bool
    supportsFileUpload: bool
    messageLimit: MessageLimit
    messageUsageLimit: MessageUsageLimit
    baseModelDisplayName: str
    nickname: str


class BotWithPrompt(BaseBot):
    followerCount: int
    monthlyActiveUsers: Optional[int] = None
    creator: Creator
    description: str
    poweredBy: str
    viewerIsFollower: bool
    shouldHide: bool
    shareLink: str
    promptPlaintext: str
    viewerIsCreator: bool


class FullBotData(BaseBot):
    # summed bot object from landing bot page and right side panel
    followerCount: int
    monthlyActiveUsers: None
    creator: Creator
    description: str
    poweredBy: str
    viewerIsFollower: bool
    shouldHide: bool
    shareLink: str
    promptPlaintext: str
    viewerIsCreator: bool
    isEligibleForLoggedOutUsage: bool
    model: str
    nickname: str
    uploadFileSizeLimit: int
    allowsImageAttachments: bool
    messageLimit: MessageLimit
    messageUsageLimit: MessageUsageLimit
    isOfficialBot: bool
    isApiBot: bool
    isDown: bool
    supportsFileUpload: bool
    baseModelDisplayName: str
    allowsClearContext: bool
    introduction: str
    conversationStarters: List[str]
    serverBotDependenciesLimitsString: None
    messageTimeoutSecs: int
    isPrivateBot: bool
    isLimitedAccess: bool
    shouldHideLimitedAccessTag: bool
    mayHaveSuggestedReplies: bool
    supportsResend: bool
    hasWelcomeTopics: bool
