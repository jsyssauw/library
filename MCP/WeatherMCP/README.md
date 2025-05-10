# Weather MCP Server

A Python-based Model Context Protocol (MCP) server that provides weather data from the National Weather Service API.

## Features

- `get-alerts`: Retrieve weather alerts for a specific US state
- `get-forecast`: Get weather forecast for a location using latitude and longitude

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weatherMCP.git
cd weatherMCP
```

2. Create a virtual environment and install dependencies:
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the server

```bash
python weather_server.py
```

### Example implementation

The server provides two main tools:

```python
# Get weather alerts for a state
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a state
    
    Args:
        state: Two-letter state code (e.g. CA, NY)
    
    Returns:
        Formatted weather alerts
    """
    # Implementation details in weather_server.py

# Get weather forecast for a location
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    
    Returns:
        Formatted weather forecast
    """
    # Implementation details in weather_server.py
```

## API Reference

### National Weather Service API

This project uses the National Weather Service API (https://api.weather.gov) to fetch weather data.

## License

MIT 