import os
import requests
from tkinter import *
from tkinter import messagebox
from tkinter import font

# Constants
COLORS = {
    'primary': '#2C3E50',      # Dark blue-gray
    'secondary': '#3498DB',     # Bright blue
    'accent': '#E74C3C',        # Red accent
    'card_bg': '#ECF0F1',       # Light gray
    'success': '#27AE60',       # Green
    'text_dark': '#2C3E50',
    'text_light': '#FFFFFF'
}

API_KEY = os.getenv('WEATHER_API_KEY', 'd8c4ab6753ff8af8c82c04868f77401f')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


def fetch_weather_data(city_name):
    """Fetches weather data from OpenWeatherMap API."""
    try:
        complete_url = f"{BASE_URL}appid={API_KEY}&q={city_name}"
        response = requests.get(complete_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not connect to server: {str(e)}")
        return None


def kelvin_to_celsius(kelvin):
    """Converts temperature from Kelvin to Celsius."""
    return round(kelvin - 273.15)


def create_weather_card(parent_frame, city_name, weather_data):
    """Creates a visual card with weather information."""
    main_data = weather_data['main']
    weather_desc = weather_data['weather'][0]['description']
    
    # Card container with border effect
    card_frame = Frame(parent_frame, bg=COLORS['card_bg'], relief=RAISED, borderwidth=2)
    card_frame.pack(pady=8, padx=10, fill=X)
    
    # Header with city name and close button
    header_frame = Frame(card_frame, bg=COLORS['secondary'])
    header_frame.pack(fill=X)
    
    city_label = Label(
        header_frame, 
        text=city_name.upper(), 
        font=("Helvetica", 14, "bold"),
        bg=COLORS['secondary'],
        fg=COLORS['text_light'],
        pady=8
    )
    city_label.pack(side=LEFT, padx=15)
    
    close_btn = Button(
        header_frame,
        text="✕",
        command=lambda: card_frame.pack_forget(),
        bg=COLORS['accent'],
        fg=COLORS['text_light'],
        font=("Helvetica", 12, "bold"),
        relief=FLAT,
        width=3,
        cursor="hand2"
    )
    close_btn.pack(side=RIGHT, padx=5, pady=5)
    
    # Weather info container
    info_frame = Frame(card_frame, bg=COLORS['card_bg'])
    info_frame.pack(fill=BOTH, padx=15, pady=10)
    
    # Temperature (bigger and highlighted)
    temp_label = Label(
        info_frame,
        text=f"{kelvin_to_celsius(main_data['temp'])}°C",
        font=("Helvetica", 32, "bold"),
        bg=COLORS['card_bg'],
        fg=COLORS['secondary']
    )
    temp_label.pack()
    
    # Weather description
    desc_label = Label(
        info_frame,
        text=weather_desc.capitalize(),
        font=("Helvetica", 11, "italic"),
        bg=COLORS['card_bg'],
        fg=COLORS['text_dark']
    )
    desc_label.pack(pady=(0, 10))
    
    # Additional info in a grid
    details_frame = Frame(info_frame, bg=COLORS['card_bg'])
    details_frame.pack()
    
    details = [
        ("💧 Humidity:", f"{round(main_data['humidity'])}%"),
        ("🌡️ Pressure:", f"{round(main_data['pressure'])} hPa"),
        ("🌡️ Feels like:", f"{kelvin_to_celsius(main_data['feels_like'])}°C")
    ]
    
    for i, (label_text, value_text) in enumerate(details):
        label = Label(
            details_frame,
            text=label_text,
            font=("Helvetica", 9),
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        )
        label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
        
        value = Label(
            details_frame,
            text=value_text,
            font=("Helvetica", 9, "bold"),
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        )
        value.grid(row=i, column=1, sticky='e', padx=5, pady=2)


def add_city():
    """Adds a new city to the weather panel."""
    city_name = city_entry.get().strip()
    
    if not city_name:
        messagebox.showwarning("Warning", "Please enter a city name")
        return
    
    weather_data = fetch_weather_data(city_name)
    
    if weather_data and weather_data.get('cod') != 404:
        create_weather_card(cities_frame, city_name, weather_data)
        city_entry.delete(0, END)
    else:
        messagebox.showerror("Error", f"City not found: {city_name}")


# Main window configuration
root = Tk()
root.title("Weather App")
root.geometry("400x650")
root.configure(bg=COLORS['primary'])
root.resizable(False, False)

# Title
title_label = Label(
    root,
    text="🌤️ Weather App",
    font=("Helvetica", 20, "bold"),
    bg=COLORS['primary'],
    fg=COLORS['text_light'],
    pady=15
)
title_label.pack()

# Input container
input_frame = Frame(root, bg=COLORS['primary'])
input_frame.pack(pady=10)

# City input field
city_entry = Entry(
    input_frame,
    font=("Helvetica", 12),
    relief=FLAT,
    bg=COLORS['text_light'],
    fg=COLORS['text_dark'],
    width=25,
    borderwidth=3
)
city_entry.pack(side=LEFT, padx=5, ipady=8)
city_entry.bind('<Return>', lambda e: add_city())
city_entry.focus()

# Add button
add_btn = Button(
    input_frame,
    text="Add",
    command=add_city,
    bg=COLORS['success'],
    fg=COLORS['text_light'],
    font=("Helvetica", 12, "bold"),
    relief=FLAT,
    cursor="hand2",
    width=8,
    borderwidth=0
)
add_btn.pack(side=LEFT, ipady=5)

# Cities container with scrollbar
container_frame = Frame(root, bg=COLORS['primary'])
container_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Canvas for scrolling
canvas = Canvas(container_frame, bg=COLORS['primary'], highlightthickness=0)
scrollbar = Scrollbar(container_frame, orient=VERTICAL, command=canvas.yview)
cities_frame = Frame(canvas, bg=COLORS['primary'])

cities_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=cities_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Footer
footer_label = Label(
    root,
    text="Powered by OpenWeatherMap API",
    font=("Helvetica", 8),
    bg=COLORS['primary'],
    fg=COLORS['text_light'],
    pady=5
)
footer_label.pack(side=BOTTOM)

root.mainloop()