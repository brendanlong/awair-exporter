# Awair API Examples

## Authentication

All requests require a Bearer token in the Authorization header.

## Get User Devices

```python
import requests

url = "https://developer-apis.awair.is/v1/users/self/devices"

payload={}
headers = {
  'Authorization': 'Bearer example-token'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

### Response

```json
{
  "devices": [
    {
      "name": "My Awair",
      "latitude": 37.77,
      "preference": "GENERAL",
      "timezone": "US/Pacific",
      "roomType": "BEDROOM",
      "deviceType": "awair",
      "longitude": -122.42,
      "spaceType": "HOME",
      "deviceUUID": "awair_0",
      "deviceId": 0,
      "locationName": "My Home"
    },
    {
      "name": "My Awair v2",
      "latitude": 37.77,
      "preference": "GENERAL",
      "timezone": "US/Pacific",
      "roomType": "BATHROOM",
      "deviceType": "awair-r2",
      "longitude": -122.42,
      "spaceType": "HOME",
      "deviceUUID": "awair-r2_0",
      "deviceId": 0,
      "locationName": "My Home"
    }
  ]
}
```

## Get 15-Minute Average Air Quality Data

### Parameters

- **from**: Start of time range. If time range given is greater than maximum range (7 days), then only 7 days will be returned, and the rest will need to be made in separate calls with your own pagination method.
  - Type: ISO 8601 Date, Time, or DateTime
  - Default: 30 Minutes before current DateTime

- **to**: End of time range. See from parameter description.
  - Type: ISO 8601 Date, Time, or DateTime
  - Default: current DateTime

- **limit**: Number of AirData points returned from the supplied time range. Maximum: ~672
  - Type: Integer
  - Default: 672

- **desc**: Return AirData in descending order before the to (true) or after the from (false) datetime. Default of true returns AirData descending from the to parameter (Current DateTime, if to is not supplied). Not to be confused with the sort order.
  - Type: Boolean
  - Default: true

- **fahrenheit**: Return Temperature in Fahrenheit
  - Type: Boolean
  - Default: false

### Request

```python
import requests

url = "https://developer-apis.awair.is/v1/users/self/devices/device_type/device_id/air-data/15-min-avg?from=from&to=to&limit=limit&desc=desc&fahrenheit=fahrenheit"

payload={}
headers = {
  'Authorization': 'Bearer example-token'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

### Response

```json
{
  "data": [
    {
      "timestamp": "2019-04-01T23:45:00.000Z",
      "score": 82.43831125895183,
      "sensors": [
        {
          "comp": "temp",
          "value": 18.82273991902669
        },
        {
          "comp": "humid",
          "value": 62.596815745035805
        },
        {
          "comp": "co2",
          "value": 418.74598185221356
        },
        {
          "comp": "voc",
          "value": 147.99961853027344
        },
        {
          "comp": "pm25",
          "value": 3.799999952316284
        }
      ],
      "indices": [
        {
          "comp": "temp",
          "value": -1
        },
        {
          "comp": "humid",
          "value": 1.9333333174387615
        },
        {
          "comp": "co2",
          "value": 0
        },
        {
          "comp": "voc",
          "value": 0
        },
        {
          "comp": "pm25",
          "value": 0
        }
      ]
    },
    {
      "timestamp": "2019-04-01T23:30:00.000Z",
      "score": 79.22222137451172,
      "sensors": [
        {
          "comp": "temp",
          "value": 18.723111470540363
        },
        {
          "comp": "humid",
          "value": 66.42177836100261
        },
        {
          "comp": "co2",
          "value": 418.8555501302083
        },
        {
          "comp": "voc",
          "value": 156.78888956705728
        },
        {
          "comp": "pm25",
          "value": 4.6555555661519366
        }
      ],
      "indices": [
        {
          "comp": "temp",
          "value": -1
        },
        {
          "comp": "humid",
          "value": 2.8111111323038735
        },
        {
          "comp": "co2",
          "value": 0
        },
        {
          "comp": "voc",
          "value": 0
        },
        {
          "comp": "pm25",
          "value": 0
        }
      ]
    },
    {
      "timestamp": "2019-04-01T23:15:00.000Z",
      "score": 78.07777659098308,
      "sensors": [
        {
          "comp": "temp",
          "value": 18.63188870747884
        },
        {
          "comp": "humid",
          "value": 68.88966878255208
        },
        {
          "comp": "co2",
          "value": 416.23333740234375
        },
        {
          "comp": "voc",
          "value": 162.16666666666666
        },
        {
          "comp": "pm25",
          "value": 5.5
        }
      ],
      "indices": [
        {
          "comp": "temp",
          "value": -1
        },
        {
          "comp": "humid",
          "value": 3
        },
        {
          "comp": "co2",
          "value": 0
        },
        {
          "comp": "voc",
          "value": 0
        },
        {
          "comp": "pm25",
          "value": 0
        }
      ]
    },
    {
      "timestamp": "2019-04-01T23:00:00.000Z",
      "score": 78.05555470784505,
      "sensors": [
        {
          "comp": "temp",
          "value": 18.61400032043457
        },
        {
          "comp": "humid",
          "value": 68.95733133951823
        },
        {
          "comp": "co2",
          "value": 410.8444315592448
        },
        {
          "comp": "voc",
          "value": 144.14444478352866
        },
        {
          "comp": "pm25",
          "value": 5.788888931274414
        }
      ],
      "indices": [
        {
          "comp": "temp",
          "value": -1
        },
        {
          "comp": "humid",
          "value": 3
        },
        {
          "comp": "co2",
          "value": 0
        },
        {
          "comp": "voc",
          "value": 0
        },
        {
          "comp": "pm25",
          "value": 0
        }
      ]
    }
  ]
}
```

### Notes

- Maximum time range of AirData points returned: 7 days (~672 data points of 15 minute averaged blocks)
- For longer date ranges, you'll need to make multiple requests with pagination

## Data Granularity Endpoints

The API supports different granularity levels:

- `/air-data/raw` - Raw sensor data
- `/air-data/5-min-avg` - 5-minute averages
- `/air-data/15-min-avg` - 15-minute averages

All endpoints follow the same URL pattern:

```
https://developer-apis.awair.is/v1/users/self/devices/{device_type}/{device_id}/air-data/{granularity}
```
