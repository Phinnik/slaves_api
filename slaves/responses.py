from typing import List, Any
from pydantic import BaseModel, Field

from slaves.dtypes import User


class ResponseBase(BaseModel):
    ...


class ResponseUser(ResponseBase, User):
    ...


class ResponseStart(ResponseBase):
    me: User = Field(...)
    share_url: str = Field(...)
    duels: List[Any] = Field(None)
    slaves: List[User] = Field(None)
    slaves_profit_per_min: int = Field(None)
    just_slave: bool = Field(None)


class ResponseUsers(ResponseBase):
    users: List[User]


class ResponseSlaveList(ResponseBase):
    slaves: List[User]


class ResponseSaleSlave(ResponseUser):
    ...


class ResponseBuySlave(ResponseUser):
    ...


class ResponseBuyFetter(ResponseUser):
    ...


class ResponseJobSlave(ResponseBase):
    slave: User


class UserTopItem(ResponseBase):
    id: int
    slaves_count: int


class ResponseTopUsers(ResponseBase):
    list: List[UserTopItem]
