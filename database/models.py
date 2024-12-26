from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    id: str
    content: str
    from_user_id: int
    to_user_id: int
    publish_timestamp: datetime
    edit_timestamp: Optional[datetime] = None


class MessageCreateRequest(BaseModel):
    content: str
    from_user_id: int
    to_user_id: int
