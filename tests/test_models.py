"""Tests for Pydantic models."""

from datetime import datetime

from awair_exporter.models import (
    CSVDataPoint,
    Device,
)


def test_device_model() -> None:
    """Test Device model parsing."""
    device_data = {
        "deviceId": 12345,
        "deviceUUID": "awair_12345",
        "deviceType": "awair-r2",
        "name": "Living Room",
        "roomType": "LIVING_ROOM",
        "spaceType": "HOME",
        "timezone": "US/Pacific",
        "locationName": "My Home",
        "latitude": 37.77,
        "longitude": -122.42,
        "preference": "GENERAL",
    }

    device = Device.model_validate(device_data)
    assert device.device_id == 12345
    assert device.name == "Living Room"
    assert device.device_type == "awair-r2"


def test_csv_data_point() -> None:
    """Test CSVDataPoint model."""
    csv_point = CSVDataPoint(
        timestamp=datetime(2024, 1, 15, 10, 0),
        temperature=22.3,
        humidity=45.2,
        co2=412.0,
        voc=150.0,
        pm25=8.3,
        score=95.0,
        device_id=12345,
        device_name="Living Room",
    )

    assert csv_point.temperature == 22.3
    assert csv_point.device_name == "Living Room"
