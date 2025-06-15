#!/usr/bin/env python3
"""CLI script for exporting Awair sensor data."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

import click

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awair_exporter.client import AwairAPIClient
from awair_exporter.config import get_settings
from awair_exporter.exporter import generate_filename, write_csv_data


@click.group()
def cli() -> None:
    """Awair data exporter CLI."""
    pass


@cli.command("list-devices")
def list_devices() -> None:
    """List all available Awair devices."""
    settings = get_settings()
    client = AwairAPIClient(settings)
    devices = client.get_devices()

    if not devices:
        click.echo("No devices found.")
        return

    for device in devices:
        click.echo(f"Device ID: {device.device_id}")
        click.echo(f"  Name: {device.name}")
        click.echo(f"  Type: {device.device_type}")
        click.echo(f"  UUID: {device.device_uuid}")
        click.echo()


@cli.command("get-data")
@click.option("--device-id", type=int, help="Device ID to export data for")
@click.option("--all-devices", is_flag=True, help="Export data for all devices")
@click.option(
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date (YYYY-MM-DD format)",
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date (YYYY-MM-DD format)",
)
@click.option(
    "--granularity",
    type=click.Choice(["raw", "5-min-avg", "15-min-avg"]),
    default="15-min-avg",
    help="Data granularity",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    help="Output CSV file path (auto-generated if not specified)",
)
def get_data(
    device_id: int | None,
    all_devices: bool,
    start_date: datetime | None,
    end_date: datetime | None,
    granularity: str,
    output: Path | None,
) -> None:
    """Export air quality data to CSV."""
    settings = get_settings()
    client = AwairAPIClient(settings)

    # Set default dates
    end_dt = end_date or datetime.now()
    start_dt = start_date or (end_dt - timedelta(days=7))

    # Validate date range
    if start_dt >= end_dt:
        click.echo("Error: Start date must be before end date", err=True)
        sys.exit(1)

    # Get devices to process
    if all_devices:
        devices = client.get_devices()
        if not devices:
            click.echo("No devices found.")
            return
    elif device_id is not None:
        all_devices_list = client.get_devices()
        devices = [d for d in all_devices_list if d.device_id == device_id]
        if not devices:
            click.echo(f"Device with ID {device_id} not found.")
            return
    else:
        click.echo("Error: Must specify either --device-id or --all-devices", err=True)
        sys.exit(1)

    # Process each device
    for device in devices:
        click.echo(f"Exporting data for device: {device.name} ({device.device_id})")

        # Get data with chunking
        responses = client.get_air_data_chunked(
            device_type=device.device_type,
            device_id=device.device_id,
            granularity=granularity,
            start_date=start_dt,
            end_date=end_dt,
        )

        # Determine output file
        if output and len(devices) == 1:
            output_path = output
        else:
            filename = generate_filename(device, granularity, start_dt, end_dt)
            output_path = Path(filename)

        # Write CSV
        write_csv_data(responses, device, output_path)
        click.echo(f"Data exported to: {output_path}")


if __name__ == "__main__":
    cli()
