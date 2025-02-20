import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# API Key (Replace with your own API key from OpenWeatherMap)
API_KEY = ""
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Function to update digital clock
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=f"🕒 {current_time}")
    root.after(1000, update_clock)

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data["cod"] != "200":
        messagebox.showerror("Error", "City not found!")
        return
    
    today_temp = data["list"][0]["main"]["temp"]
    today_desc = data["list"][0]["weather"][0]["description"].capitalize()
    result_label.config(text=f"🌳 {city} \n🌡 Temperature: {today_temp}°C \n🌦 Condition: {today_desc}")
    
    days = []
    temps = []
    
    for i in range(0, 40, 8):  # Get one data point per day (API returns 3-hour intervals)
        day_data = data["list"][i]
        day_temp = day_data["main"]["temp"]
        day_time = day_data["dt_txt"].split(" ")[0]
        days.append(day_time)
        temps.append(day_temp)
    
    plot_graph(days, temps)

# Function to plot temperature graph
def plot_graph(days, temps):
    for widget in graph_frame.winfo_children():
        widget.destroy()
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(days, temps, marker='o', linestyle='-', color='#228B22', label='Temperature (°C)')
    ax.set_title("🌿 10-Day Temperature Forecast", color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Temperature (°C)", color='white')
    ax.grid(True, color='#6B8E23')
    ax.legend()
    ax.set_facecolor("#013220")
    fig.patch.set_facecolor("#013220")
    
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("🌲 Forest-Themed Weather App")
root.geometry("700x800")
root.configure(bg="#013220")  # Dark forest green

main_frame = tk.Frame(root, bg="#013220", bd=5, relief="ridge")
main_frame.pack(padx=40, pady=40, fill="both", expand=True)

clock_label = tk.Label(main_frame, text="", font=("Arial", 20, "bold"), bg="#013220", fg="white")
clock_label.pack(pady=10)
update_clock()

city_label = tk.Label(main_frame, text="🌍 Enter City Name:", font=("Arial", 14, "bold"), bg="#013220", fg="white")
city_label.pack(pady=10)

city_entry = tk.Entry(main_frame, width=30, font=("Arial", 14), bg="#228B22", fg="white", insertbackground="white")
city_entry.pack()

fetch_button = tk.Button(main_frame, text="☁ Get Weather", font=("Arial", 14, "bold"), bg="#6B8E23", fg="white", command=get_weather)
fetch_button.pack(pady=10)

result_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="#013220", fg="white", justify="left")
result_label.pack(pady=10)

graph_frame = tk.Frame(main_frame, bg="#013220", bd=5, relief="ridge")
graph_frame.pack(padx=30, pady=20, fill="both", expand=True)

root.mainloop()
