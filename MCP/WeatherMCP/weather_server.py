from typing import Any
import httpx
import asyncio
import sys
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool

# Initialize FastMCP server
server_name = "WeatherServer"
server_version = "1.0.0"
mcp = FastMCP(server_name)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a state
    
    Args:
        state: Two-letter state code (e.g. CA, NY)
    
    Returns:
        Formatted weather alerts
    """
    if len(state) != 2:
        return "Error: Please provide a valid two-letter state code"
    
    state = state.upper()
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    
    alerts_data = await make_nws_request(url)
    if not alerts_data:
        return "Unable to fetch alerts data for this state."
    
    features = alerts_data.get("features", [])
    if not features:
        return f"No active weather alerts for {state}."
    
    formatted_alerts = []
    for feature in features:
        props = feature.get("properties", {})
        alert = f"""
Alert: {props.get('event', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Headline: {props.get('headline', 'No headline')}
Description: {props.get('description', 'No description')[:200]}{'...' if len(props.get('description', '')) > 200 else ''}
"""
        formatted_alerts.append(alert)
    
    return "\n---\n".join(formatted_alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    
    Returns:
        Formatted weather forecast
    """
    # First, we need to get the forecast office that serves this point
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    
    points_data = await make_nws_request(points_url)
    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
    if not forecast_data:
        return "Unable to fetch detailed forecast."
    
    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)
    
    return "\n---\n".join(forecasts)

def print_server_info():
    """Display detailed information about the MCP server"""
    divider = "=" * 60
    
    # Create server info display
    server_info = f"""
{divider}
🌦️  MCP WEATHER SERVER RUNNING  🌦️
{divider}
Server Name: {server_name}
Server Version: {server_version}
Transport: stdio
API Endpoint: {NWS_API_BASE}

Available Tools:
  - get-alerts: Get weather alerts for a state
  - get-forecast: Get weather forecast for a location

Server is ready to process requests!
{divider}
"""
    print(server_info, file=sys.stderr)

if __name__ == "__main__":
    print_server_info()
    mcp.run(transport="stdio") 