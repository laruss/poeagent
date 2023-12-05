from typing import Literal, Optional


class RequestParams:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id")
        self.metadata: dict = kwargs.get("metadata", {})
        self.name: str = kwargs.get("name")
        self.operationKind: Literal["query", "mutation", "subscription"] = kwargs.get("operationKind")
        self.text: Optional[str] = kwargs.get("text")

    def dict_(self):
        return {
            "id": self.id,
            "metadata": self.metadata,
            "name": self.name,
            "operationKind": self.operationKind,
            "text": self.text
        }
