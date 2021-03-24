from typing import List, Optional
from pydantic import BaseModel, Field


class Job(BaseModel):
    name: str = Field(None)


class User(BaseModel):
    balance: int = Field(None)
    chicken_mark: bool = Field(None)
    chicken_mark_clean: int = Field(None)
    duel_count: int = Field(None)
    duel_reject: int = Field(None)
    duel_win: int = Field(None)
    fetter_hour: int = Field(None)
    fetter_price: int = Field(None)
    fetter_to: int = Field(None)
    id: int = Field(None)
    item_type: str = Field(None)
    job: Job = Field(None)
    master_id: int = Field(None)
    price: int = Field(None)
    profit_per_min: int = Field(None)
    rating_position: int = Field(None)
    sale_price: int = Field(None)
    slaves_count: int = Field(None)
    slaves_profit_per_min: int = Field(None)
    was_in_app: bool = Field(None)
