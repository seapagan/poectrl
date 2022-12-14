"""Base Schemas used in the API."""
from typing import List

from pydantic import BaseModel


class DeviceSettingsBaseSchema(BaseModel):
    """The base schema for a single device."""

    user: str
    password: str


class SingleDeviceSchema(BaseModel):
    """Schema for Device plus IP."""

    ip: DeviceSettingsBaseSchema


class DevicesSchema(BaseModel):
    """Schema for a dictionary of devices."""

    devices: List[SingleDeviceSchema]


class ProfileSchema(BaseModel):
    """The base schema for a single profile."""

    name: str
