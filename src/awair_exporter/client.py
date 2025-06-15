"""Awair API client."""

from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import urljoin

import requests

from .config import Settings
from .models import AirDataResponse, Device, DeviceListResponse


class AwairAPIClient:
    """Client for interacting with the Awair API."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the API client.

        Args:
            settings: Application settings containing API credentials
        """
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {settings.awair_access_token}",
                "Content-Type": "application/json",
            }
        )

    def get_devices(self) -> List[Device]:
        """Get list of user's devices.

        Returns:
            List of user's Awair devices

        Raises:
            requests.HTTPError: If the API request fails
        """
        url = urljoin(self.settings.awair_base_url, "/v1/users/self/devices")
        response = self.session.get(url)
        response.raise_for_status()

        device_list = DeviceListResponse.model_validate(response.json())
        return device_list.devices

    def get_air_data(
        self,
        device_type: str,
        device_id: int,
        granularity: str = "15-min-avg",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 672,
        desc: bool = True,
        fahrenheit: bool = False,
    ) -> AirDataResponse:
        """Get air quality data for a device.

        Args:
            device_type: Type of device (e.g., "awair-r2", "awair-element")
            device_id: ID of the device
            granularity: Data granularity ("raw", "5-min-avg", "15-min-avg")
            start_date: Start of time range (defaults to 30 minutes ago)
            end_date: End of time range (defaults to now)
            limit: Number of data points to return (max 672)
            desc: Return data in descending order
            fahrenheit: Return temperature in Fahrenheit

        Returns:
            Air quality data response

        Raises:
            requests.HTTPError: If the API request fails
        """
        url = urljoin(
            self.settings.awair_base_url,
            f"/v1/users/self/devices/{device_type}/{device_id}/air-data/{granularity}",
        )

        params: dict[str, str | int | bool] = {
            "limit": limit,
            "desc": desc,
            "fahrenheit": fahrenheit,
        }

        if start_date:
            params["from"] = start_date.isoformat()

        if end_date:
            params["to"] = end_date.isoformat()

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return AirDataResponse.model_validate(response.json())

    def get_air_data_chunked(
        self,
        device_type: str,
        device_id: int,
        granularity: str = "15-min-avg",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        chunk_days: int = 7,
    ) -> List[AirDataResponse]:
        """Get air quality data in chunks to handle API limits.

        The API has a maximum range of 7 days for most endpoints.
        This method splits larger date ranges into multiple requests.

        Args:
            device_type: Type of device
            device_id: ID of the device
            granularity: Data granularity
            start_date: Start of time range
            end_date: End of time range
            chunk_days: Number of days per chunk (max 7)

        Returns:
            List of air quality data responses
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)
        if not end_date:
            end_date = datetime.now()

        chunk_days = min(chunk_days, 7)  # API limit
        responses = []

        current_start = start_date
        while current_start < end_date:
            current_end = min(current_start + timedelta(days=chunk_days), end_date)

            response = self.get_air_data(
                device_type=device_type,
                device_id=device_id,
                granularity=granularity,
                start_date=current_start,
                end_date=current_end,
            )
            responses.append(response)

            current_start = current_end

        return responses
