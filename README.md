# Awair Exporter

Export your Awair air quality sensor data to CSV format.

## Features

- OAuth 2.0 authentication support
- Export data for any date range
- Automatic chunking for large date ranges (respecting API limits)
- CSV output with all sensor data:
  - Temperature (°C)
  - Humidity (%)
  - CO2 (ppm)
  - VOC (ppb)
  - PM2.5 (μg/m³)
- Configurable via environment variables or config file

## Installation

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/awair-exporter.git
cd awair-exporter

# Install the package and dependencies
uv sync

# Activate the virtual environment (or use direnv)
source .venv/bin/activate
```

## Configuration

Create a `.env` file in the project root (this file is gitignored):

```env
AWAIR_CLIENT_ID=your_client_id
AWAIR_CLIENT_SECRET=your_client_secret
AWAIR_REDIRECT_URI=your_redirect_uri
AWAIR_ACCESS_TOKEN=your_access_token
```

Alternatively, you can export these as environment variables.

## Usage

All commands assume you've activated the virtual environment with `source .venv/bin/activate` or are using direnv.

### First, list your devices to get device IDs

```bash
scripts/awair-export.py list-devices
```

Output:

```
Device ID: 12345
  Name: Living Room
  Type: awair-r2
  UUID: ABC123-DEF456

Device ID: 67890
  Name: Bedroom
  Type: awair-element
  UUID: GHI789-JKL012
```

### Export data for a specific device

#### Basic usage (export last 7 days)

```bash
scripts/awair-export.py get-data --device-id 12345
```

#### Export specific date range

```bash
scripts/awair-export.py get-data --device-id 12345 --start-date 2024-01-01 --end-date 2024-01-31
```

#### Export to specific file

```bash
scripts/awair-export.py get-data --device-id 12345 --output sensor-data.csv
```

#### Export with specific granularity

```bash
scripts/awair-export.py get-data --device-id 12345 --granularity 5min  # Options: raw, 5min, 15min
```

#### Export all devices to separate files

```bash
scripts/awair-export.py get-data --all-devices
```

## Output Format

The CSV output includes the following columns:

- `timestamp`: ISO 8601 formatted timestamp
- `temperature`: Temperature in Celsius
- `humidity`: Relative humidity percentage
- `co2`: CO2 in parts per million
- `voc`: Total VOCs in parts per billion
- `pm25`: PM2.5 in micrograms per cubic meter
- `score`: Awair score (0-100)
- `device_id`: Device identifier
- `device_name`: Device name

Example output:

```csv
timestamp,temperature,humidity,co2,voc,pm25,score,device_id,device_name
2024-01-15T10:00:00Z,22.3,45.2,412,150,8.3,95,12345,Living Room
2024-01-15T10:05:00Z,22.4,45.1,415,152,8.5,94,12345,Living Room
```

## API Limits

The Awair API has the following daily limits for hobbyist tier:

- Latest data: 300 requests/day
- Raw data: 500 requests/day
- 5-minute averages: 300 requests/day
- 15-minute averages: 100 requests/day

The exporter automatically manages these limits by chunking large date ranges into smaller requests.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.
