import requests
from tkinter import *
from tkinter import Tk, font
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen

class WeatherApp:
    def __init__(self, master: Tk):
         # base app
        self.master = master
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=19, weight=font.BOLD)
        self.create_widgets()
        
    def create_widgets(self):
        # search for city
        self.search_etr = Entry(self.master)
        self.search_btn = Button(self.master, text="Search", command=self.search_city)
        # items
        self.locat_lbl = Label(self.master, bg="blue")
        self.temp_lbl = Label(self.master, bg="blue")
        self.weather_lbl = Label(self.master, bg="blue")
        # image
        self.icon = Label(self.master, bg="blue")
        # add items
        self.search_etr.pack()
        self.search_btn.pack()
        self.locat_lbl.pack()
        self.temp_lbl.pack()
        self.weather_lbl.pack()
    
    def create_icon(self, icon):
        # upload the icon
        raw_data = urlopen(f"http://openweathermap.org/img/wn/{icon}@2x.png").read()
        temp_img = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(temp_img)
        self.icon["image"] = image
        self.icon.image = image
        self.icon.pack()

    def search_city(self):
        self.get_data(city=self.search_etr.get())
        self.search_etr.delete(0, 'end')
    
    def get_data(self, city="Odessa"):
        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        mode = "GET"
        querystring = {"q":{city},"lang":"en","units":"metric"}
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "32c4ac93d2msh32e94c84194df3fp166d6ajsnec3e473f2c4e"
        }

        response = requests.request(mode, url, headers=headers, params=querystring)
        response = response.json()
        self.render_data(response)

    def render_data(self, data):
        self.locat_lbl["text"] = f"{data['name']},{data['sys']['country']}"
        self.temp_lbl["text"] = f"Temp: {data['main']['temp']}\N{DEGREE SIGN}\nFeels like: {data['main']['feels_like']}\N{DEGREE SIGN}"
        self.weather_lbl["text"] = f"Weather: {data['weather'][0]['description'].capitalize()}"
        self.create_icon(data["weather"][0]["icon"])