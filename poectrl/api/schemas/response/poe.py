"""Response Schemas for the PoE Manager."""

from typing import List

from pydantic import BaseModel


class ListResponse(BaseModel):
    """Schema for List route response."""

    profiles: List[str]


class ApplyResponse(BaseModel):
    """Schema for Apply route response."""

    detail: str
