from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .send_message_data import MessageData, Chat


class WsMessage(BaseModel):
    id: str
    messageId: int
    creationTime: int
    clientNonce: Optional[str]
    state: str
    text: str
    author: str
    contentType: str
    sourceType: str
    attachmentTruncationState: str
    attachments: List
    vote: None
    suggestedReplies: List
    hasCitations: bool
    field__isNode: str = Field(..., alias='__isNode')
    textLengthOnCancellation: None
    humanMessage: Optional[MessageData] = None
    chat: Optional[Chat] = None
