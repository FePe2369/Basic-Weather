# Weather App

A simple and elegant desktop weather application built with Python and Tkinter.

## Features

- Search weather by city name
- Display temperature, humidity, and pressure
- Add multiple cities to compare
- Clean and modern UI
- Press Enter to add cities quickly

## Requirements

```bash
pip install requests
```

## Usage

1. Run the application:

```bash
python weather_app.py
```

2. Enter a city name and click "Add" or press Enter
3. View weather information for multiple cities
4. Click the ✕ button to remove a city card

## API Key

The app uses OpenWeatherMap API. You can set your own API key using environment variables:

```bash
# Linux/Mac
export WEATHER_API_KEY="your_api_key_here"

# Windows (CMD)
set WEATHER_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:WEATHER_API_KEY="your_api_key_here"
```

Get your free API key at: https://openweathermap.org/api

## Screenshot

The app displays:

- City name in header
- Large temperature display
- Weather description
- Humidity percentage
- Atmospheric pressure
- "Feels like" temperature

## License

Free to use and modify.
