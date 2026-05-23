from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="My Item")
    description: Optional[str] = Field(None, max_length=500, example="Item description")
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
