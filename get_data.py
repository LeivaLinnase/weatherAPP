import requests
import pandas as pd

API_KEY = '69d6ced8d21c41689bf45419240312'
BASE_URL = "http://api.weatherapi.com/v1"


def get_weather(city):
    endpoint = f"{BASE_URL}/current.json"  # Endpoint for current weather data
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "no",
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None


def make_csv(data, filename="weather_data.csv"):
    try:
        df = pd.DataFrame.from_dict(data, orient='index').reset_index()

        # Rename the 'index' column to 'City'
        df.rename(columns={"index": "City"}, inplace=True)

        df.to_csv(filename, index=False, encoding="utf-8")

        print(f"\nWeather data saved to {filename} successfully!")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    city_list = ['Tallinn', 'Stockholm', 'Bangkok', 'Ao Nang', 'Pattaya', 'Koh Samui', 'Buri Ram', 'Chiang Mai']
    results = {}

    for city in city_list:
        print(f"Fetching weather data for {city}...")
        weather_data = get_weather(city)

        if weather_data:
            results[city] = {
                "Temperature (°C)": weather_data['current']['temp_c'],
                "Condition": weather_data['current']['condition']['text'],
                "Humidity (%)": weather_data['current']['humidity'],
                # "Country": weather_data['location']['country']
                "Wind Speed (kph)": weather_data['current']['wind_kph'],
                "Precipitation": weather_data['current']['precip_mm'],
                "Is Day": weather_data['current']['is_day'],
                "UV-index": weather_data['current']['uv']
            }

    # Print results as JSON
    print("\nWeather Data for Cities:")
    for city, data in results.items():
        print(f"{city}: {data}")

    make_csv(results)


