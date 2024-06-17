import requests

# NWS API endpoint for getting weather information based on latitude and longitude
NWS_ENDPOINT = "https://api.weather.gov/points/{lat},{lon}"

# Example location: Gifford, FL
latitude = "27.6555"
longitude = "-80.4179"

# Create the URL by substituting latitude and longitude into the endpoint template
url = NWS_ENDPOINT.format(lat=latitude, lon=longitude)

# Headers for the HTTP request
headers = {
    "User-Agent": "weather.py (chris.hinson@proton.me)"
}

try:
    # Send a GET request to the API endpoint with specified headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response into Python dictionary
        data = response.json()

        # Extract general location information from the JSON response
        cwa = data["properties"]["cwa"]
        forecast_office = data["properties"]["forecastOffice"]
        grid_id = data["properties"]["gridId"]
        grid_x = data["properties"]["gridX"]
        grid_y = data["properties"]["gridY"]
        forecast_url = data["properties"]["forecast"]

        # Extract relative location information
        relative_location = data["properties"]["relativeLocation"]
        city = relative_location["properties"]["city"]
        state = relative_location["properties"]["state"]
        distance = relative_location["properties"]["distance"]["value"]
        bearing = relative_location["properties"]["bearing"]["value"]

        # Extract forecast related information
        forecast_zone = data["properties"]["forecastZone"]
        county = data["properties"]["county"]
        fire_weather_zone = data["properties"]["fireWeatherZone"]
        time_zone = data["properties"]["timeZone"]
        radar_station = data["properties"]["radarStation"]

        # Print all extracted information
        print("Location Information:")
        print(f"CWA: {cwa}")
        print(f"Forecast Office: {forecast_office}")
        print(f"Grid ID: {grid_id}")
        print(f"Grid Coordinates (X, Y): {grid_x}, {grid_y}")
        print()
        print("Relative Location Information:")
        print(f"City: {city}")
        print(f"State: {state}")
        print(f"Distance: {distance} meters")
        print(f"Bearing: {bearing} degrees")
        print()
        print("Forecast Related Information:")
        print(f"Forecast Zone: {forecast_zone}")
        print(f"County: {county}")
        print(f"Fire Weather Zone: {fire_weather_zone}")
        print(f"Time Zone: {time_zone}")
        print(f"Radar Station: {radar_station}")
        print()

        # Fetch and print the general forecast if forecast URL is available
        if forecast_url:
            response_forecast = requests.get(forecast_url, headers=headers)
            if response_forecast.status_code == 200:
                forecast_data = response_forecast.json()
                periods = forecast_data.get("properties", {}).get("periods", [])
                if periods:
                    print("General Forecast:")
                    for period in periods:
                        print(f"- {period['name']}: {period['detailedForecast']}")
                else:
                    print("No forecast periods found.")
            else:
                print(f"Error fetching general forecast data: {response_forecast.status_code}")
        else:
            print("No general forecast URL found.")

    else:
        # If the initial request fails (status code not 200), print error message
        print(f"Error fetching point data: {response.status_code}")
        print(response.text)  # Print the response content for debugging

except requests.exceptions.RequestException as e:
    # Handle any exceptions that occur during the request
    print(f"Request error: {e}")
