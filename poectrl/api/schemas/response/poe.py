"""Response Schemas for the PoE Manager."""

from typing import List

from pydantic import BaseModel


class ListResponse(BaseModel):
    profiles: List[str]
