# Weather App

A small desktop weather app built with Python and Tkinter, using the OpenWeatherMap API.

## Features

- Search current weather by city name
- Shows temperature, "feels like", humidity and pressure
- Compare several cities side by side
- Add a city with the button or by pressing Enter

## Requirements

```bash
pip install requests
```

(Tkinter ships with the Python standard library.)

## API key

The app reads your OpenWeatherMap key from an environment variable, so no secret is committed to the repo:

```bash
# Linux/macOS
export WEATHER_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:WEATHER_API_KEY="your_api_key_here"
```

Get a free key at <https://openweathermap.org/api>.

## Running it

```bash
python main.py
```
