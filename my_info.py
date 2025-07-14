# my_info.py
#
# Part of the AI News Reporter project.
# This file defines a FastMCP server that provides two tools:
# 1. get_weather: Returns real-time weather information for any location using Open-Meteo and Nominatim (no API key required).
# 2. get_news: Returns the latest news headlines for a topic using SerpAPI (requires SERPAPI_KEY in .env).
#
# The server is started at the end of the file and listens for tool calls from the client.

import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file (for SERPAPI_KEY)
load_dotenv()

# Create the FastMCP server instance
mcp = FastMCP("MyInfo")

# Get the SerpAPI key from environment variables (if available)
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get the current weather for a given location using Open-Meteo and Nominatim.
    1. Geocodes the location name to latitude/longitude using Nominatim (OpenStreetMap).
    2. Fetches current weather data from Open-Meteo for those coordinates.
    3. Returns a user-friendly weather summary.
    """
    # Step 1: Geocode location to lat/lon using Nominatim
    geocode_url = "https://nominatim.openstreetmap.org/search"
    geocode_params = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    geocode_resp = requests.get(geocode_url, params=geocode_params, headers={"User-Agent": "ai-news-reporter"})
    if geocode_resp.status_code != 200 or not geocode_resp.json():
        return f"Could not find location: {location}"
    geo = geocode_resp.json()[0]
    lat, lon = geo["lat"], geo["lon"]

    # Step 2: Fetch weather from Open-Meteo
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }
    weather_resp = requests.get(weather_url, params=weather_params)
    if weather_resp.status_code != 200:
        return f"Could not fetch weather for {location}."
    weather = weather_resp.json().get("current_weather")
    if not weather:
        return f"No weather data available for {location}."
    
    temp = weather["temperature"]
    wind = weather["windspeed"]
    desc = f"The current temperature in {location.title()} is {temp}°C with wind speed {wind} km/h."
    return desc

@mcp.tool()
async def get_news(topic: str) -> str:
    """
    Fetch the latest news headlines for a given topic using SerpAPI.
    Requires SERPAPI_KEY to be set in the .env file.
    Returns a formatted string with the top 5 headlines and their links.
    """
    if not SERPAPI_KEY:
        return "Error: SERPAPI_KEY not found in environment variables."
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": topic,
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Failed to fetch news: {response.text}"
    data = response.json()
    news_results = data.get("news_results", [])
    if not news_results:
        return f"No news found for '{topic}'."
    headlines = [f"{i+1}. {news['title']} - {news['link']}" for i, news in enumerate(news_results[:5])]
    return f"Top news for '{topic}':\n" + "\n".join(headlines)

# Start the FastMCP server when this script is run directly
if __name__ == "__main__":
    mcp.run(transport="streamable-http")