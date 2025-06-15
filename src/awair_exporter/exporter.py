"""CSV export functionality for Awair data."""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

from .models import AirDataResponse, CSVDataPoint, DataPoint, Device


def flatten_data_point(
    data_point: DataPoint,
    device: Device,
) -> CSVDataPoint:
    """Convert a DataPoint to a flattened CSVDataPoint.

    Args:
        data_point: Raw data point from API
        device: Device information

    Returns:
        Flattened data point for CSV export
    """
    # Create a mapping of sensor components to values
    sensor_values = {reading.comp: reading.value for reading in data_point.sensors}

    return CSVDataPoint(
        timestamp=data_point.timestamp,
        temperature=sensor_values.get("temp"),
        humidity=sensor_values.get("humid"),
        co2=sensor_values.get("co2"),
        voc=sensor_values.get("voc"),
        pm25=sensor_values.get("pm25"),
        score=data_point.score,
        device_id=device.device_id,
        device_name=device.name,
    )


def write_csv_data(
    responses: List[AirDataResponse],
    device: Device,
    output_file: Path,
) -> None:
    """Write air quality data to a CSV file.

    Args:
        responses: List of API responses containing air quality data
        device: Device information
        output_file: Path to output CSV file
    """
    # Flatten all data points
    csv_data_points: List[CSVDataPoint] = []
    for response in responses:
        for data_point in response.data:
            csv_data_points.append(flatten_data_point(data_point, device))

    # Sort by timestamp (oldest first)
    csv_data_points.sort(key=lambda x: x.timestamp)

    # Write to CSV
    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        if not csv_data_points:
            return

        # Get field names from the first data point
        fieldnames = list(csv_data_points[0].model_dump().keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data_point in csv_data_points:
            # Convert to dict and format timestamp
            row = data_point.model_dump()
            row["timestamp"] = data_point.timestamp.isoformat()
            writer.writerow(row)


def generate_filename(
    device: Device,
    granularity: str,
    start_date: datetime,
    end_date: datetime,
) -> str:
    """Generate a filename for the CSV export.

    Args:
        device: Device information
        granularity: Data granularity
        start_date: Start date of data
        end_date: End date of data

    Returns:
        Generated filename
    """
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    # Clean device name for filename
    clean_name = "".join(
        c for c in device.name if c.isalnum() or c in ("-", "_")
    ).strip()

    return (
        f"awair_{clean_name}_{device.device_id}_{granularity}_{start_str}_{end_str}.csv"
    )
