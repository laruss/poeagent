from __future__ import annotations

from typing import List

from pydantic import BaseModel

from .bot import OverviewBot


class Edge(BaseModel):
    cursor: str
    node: OverviewBot
    id: str


class PageInfo(BaseModel):
    endCursor: str
    hasNextPage: bool


class AvailableBotsConnection(BaseModel):
    edges: List[Edge]
    pageInfo: PageInfo
    id: str


class Viewer(BaseModel):
    hasActiveSubscription: bool
    availableBotsConnection: AvailableBotsConnection
    id: str


class Data(BaseModel):
    viewer: Viewer


class Extensions(BaseModel):
    is_final: bool


class GetBotDataResponse(BaseModel):
    data: Data
    extensions: Extensions
