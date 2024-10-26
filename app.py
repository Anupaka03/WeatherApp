import requests
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser 

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and configure labels and entry fields
city_label = tk.Label(root, text="City:")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

# Dropdown to select temperature unit
unit_label = tk.Label(root, text="Select Temperature Unit:")
unit_label.pack()
unit_var = tk.StringVar(value="Celsius")  # Default is Celsius
unit_dropdown = tk.OptionMenu(root, unit_var, "Celsius", "Fahrenheit", "Kelvin")
unit_dropdown.pack()

# Create a button to fetch weather data
fetch_button = tk.Button(root, text="Fetch Weather")
fetch_button.pack()

# Create a label to display weather information
weather_label = tk.Label(root, text="")
weather_label.pack()

# Define the function to fetch weather data
def fetch_weather():
    city = city_entry.get()
    unit = unit_var.get()
    # extract key from the configuration file 
    config_file = "config.ini"
    config = ConfigParser() 
    config.read(config_file) 
    api_key = config['Weathapp']['api']
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] != '404':
            print(data)
            temp_kelvin = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            
            # Convert temperature based on user selection
            if unit == "Celsius":
                temperature = temp_kelvin - 273.15
                temp_unit = "°C"
            elif unit == "Fahrenheit":
                temperature = (temp_kelvin - 273.15) * 9/5 + 32
                temp_unit = "°F"
            else:  # Kelvin
                temperature = temp_kelvin
                temp_unit = "K"

            # Update the weather label with detailed information
            weather_label.config(
                text=f"City: {city}\n"
                    f"Temperature: {round(temperature, 2)}{temp_unit}\n"
                    f"Weather: {weather_desc}\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"Pressure: {pressure} hPa"
            )
        else:
            weather_label.config(text="City not found")
    
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

# Set the command for the button to fetch weather data
fetch_button.config(command=fetch_weather)

# Start the GUI main loop
root.mainloop()
