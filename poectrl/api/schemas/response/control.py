"""Define response schemas for control routes."""
from pydantic import BaseModel


class ListResponseSchema(BaseModel):
    """Schema for '/list/' Response."""
