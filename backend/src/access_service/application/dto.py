from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserIdRequest:
    user_id: int

@dataclass
class NewChatUserIdRequest(UserIdRequest): ...

@dataclass
class NewMessageSendRequest:
    content: str
    user_id: int
