from typing import List, Any
from pydantic import BaseModel, Field
from slaves import dtypes


class StartResponse(BaseModel):
    me: dtypes.User = Field(...)
    share_url: str = Field(...)
    duels: List[Any] = Field(None)
    slaves: List[dtypes.User] = Field(None)
    slaves_profit_per_min: int = Field(None)
    just_slave: bool = Field(None)


class UserGetResponse(dtypes.User):
    pass


class UsersGetResponse(BaseModel):
    users: List[dtypes.User]


class SlaveListResponse(BaseModel):
    slaves: List[dtypes.User]


class BuySlaveResponse(dtypes.User):
    pass


class SaleSlaveResponse(dtypes.User):
    pass


class BuyFetterResponse(dtypes.User):
    pass


class JobSlaveResponse(BaseModel):
    slave: dtypes.User


class UserTopItem(BaseModel):
    id: int
    slaves_count: int


class TopUsersResponse(BaseModel):
    list: List[UserTopItem]
