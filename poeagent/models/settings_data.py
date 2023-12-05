from __future__ import annotations

from typing import List, Optional, Any, Union

from pydantic import BaseModel, Field


class MessageLimit(BaseModel):
    canSend: bool
    resetTime: int
    dailyBalance: Optional[int]
    dailyLimit: Optional[int]
    monthlyBalance: Optional[int]
    monthlyLimit: Optional[int]
    monthlyBalanceRefreshTime: Optional[int]
    shouldShowRemainingMessageCount: bool
    shouldShowSubscriptionRationale: bool
    id: str


class SubscriptionBot(BaseModel):
    handle: str
    limitedAccessType: str
    id: str
    displayName: str
    messageLimit: MessageLimit


class Subscription(BaseModel):
    isActive: bool
    planType: str
    id: str
    purchaseType: str
    isComplimentary: bool
    expiresTime: int
    willCancelAtPeriodEnd: bool
    isFreeTrial: bool
    purchaseRevocationReason: Optional[Any]


class AdvertisedSubscriptionBot(BaseModel):
    displayName: str
    providerName: str
    id: str


class WebSubscriptionPriceInfo(BaseModel):
    yearlyPrice: str
    id: str


class Bot(BaseModel):
    limitedAccessType: str
    displayName: str
    id: str


class Limits(BaseModel):
    id: str
    freeLimitResetTime: int
    freeLimitBalance: int
    freeLimit: int
    freeLimitResetPeriod: str
    paidLimitBalance: int
    paidLimitResetPeriod: str
    paidLimit: int
    paidLimitResetTime: int
    bot: Bot
    field__typename: str = Field(..., alias='__typename')


class Edge(BaseModel):
    cursor: str
    node: Limits
    id: str


class PageInfo(BaseModel):
    endCursor: str
    hasNextPage: bool


class MessageLimitsConnection(BaseModel):
    edges: List[Edge]
    pageInfo: PageInfo
    id: str


class PoeUser(BaseModel):
    isPoeOnlyUser: bool
    id: str
    apiKey: Optional[str]


class DefaultBot(BaseModel):
    botId: int
    id: str


class Node1(BaseModel):
    id: str
    botId: int
    displayName: str
    deletionState: str
    field__typename: str = Field(..., alias='__typename')


class Edge1(BaseModel):
    node: Node1
    cursor: str
    id: str


class AvailableBotsConnection(BaseModel):
    edges: List[Edge1]
    pageInfo: PageInfo
    id: str


class Viewer(BaseModel):
    primaryPhoneNumber: Optional[Union[str, int]]
    uid: int
    primaryEmail: str
    confirmedEmails: List[str]
    subscriptionBots: List[SubscriptionBot]
    subscription: Subscription
    useNewLimitSystem: bool
    isEligibleForWebSubscriptions: bool
    advertisedSubscriptionBots: List[AdvertisedSubscriptionBot]
    webSubscriptionPriceInfo: WebSubscriptionPriceInfo
    messageLimitsConnection: MessageLimitsConnection
    hasActiveSubscription: bool
    poeUser: PoeUser
    id: str
    defaultBot: DefaultBot
    availableBotsConnection: AvailableBotsConnection
    enableWindowsDownload: bool
    shouldOpenLinksInApp: bool
    enableLanguageSwitcher: bool


class Data(BaseModel):
    viewer: Viewer


class Extensions(BaseModel):
    is_final: bool


class SettingsResponse(BaseModel):
    data: Data
    extensions: Extensions
