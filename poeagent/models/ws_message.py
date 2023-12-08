from __future__ import annotations

from typing import Optional

from .send_message_data import MessageData, Chat


class WsMessage(MessageData):
    humanMessage: Optional[MessageData] = None
    chat: Optional[Chat] = None
