"""Pydantic models for Awair API responses."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Device(BaseModel):
    """Awair device information."""

    device_id: int = Field(alias="deviceId")
    device_uuid: str = Field(alias="deviceUUID")
    device_type: str = Field(alias="deviceType")
    name: str
    room_type: str = Field(alias="roomType")
    space_type: str = Field(alias="spaceType")
    timezone: str
    location_name: str = Field(alias="locationName")
    latitude: float
    longitude: float
    preference: str


class DeviceListResponse(BaseModel):
    """Response from the devices endpoint."""

    devices: List[Device]


class SensorReading(BaseModel):
    """Individual sensor reading."""

    comp: str  # Component name (temp, humid, co2, voc, pm25)
    value: float


class SensorIndex(BaseModel):
    """Individual sensor index value."""

    comp: str  # Component name (temp, humid, co2, voc, pm25)
    value: float


class DataPoint(BaseModel):
    """Single air quality data point."""

    timestamp: datetime
    score: float
    sensors: List[SensorReading]
    indices: List[SensorIndex]


class AirDataResponse(BaseModel):
    """Response from air data endpoints."""

    data: List[DataPoint]


class CSVDataPoint(BaseModel):
    """Flattened data point for CSV export."""

    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    co2: Optional[float] = None
    voc: Optional[float] = None
    pm25: Optional[float] = None
    score: float
    device_id: int
    device_name: str
