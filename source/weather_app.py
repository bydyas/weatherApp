import requests
from tkinter import *
from tkinter import Tk, font, messagebox
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen
from datetime import date
from time import ctime
from source.config import API

class WeatherApp:
    def __init__(self, master: Tk):
        self.master = master
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=12, weight="bold")
        self.create_widgets()

    def move_window(self,e):
        self.master.geometry(f'+{e.x_root}+{e.y_root}')

    def create_widgets(self):
        # create modified titlebar
        self.master.overrideredirect(True)
        self.titlebar = Frame(self.master, bg="#202124", bd=0, relief="raised")
        self.titlebar.bind('<B1-Motion>', self.move_window)

        self.close_btn = Button(self.titlebar, text="  ×  ", bg="#202124", fg="#e8eaed", 
                                cursor="mouse", relief="sunken", bd=0, command=self.master.quit)
        self.search_etr = Entry(self.titlebar, bg="#e8eaed", bd=0)
        self.search_btn = Button(self.titlebar, text="Search", bg="#202124", fg="#e8eaed", 
                                cursor="mouse", relief="sunken", bd=0, command=self.search_city)
        # main frame
        self.mainFrame = Frame(self.master, bg="#202124", bd=0, relief="raised")
        self.weather_lbl = Label(self.mainFrame, bg="#202124", fg="#e8eaed")
        self.icon = Label(self.mainFrame, bg="#202124")
        self.locat_lbl = Label(self.mainFrame, font=("Arial", 22), bg="#202124", fg="#e8eaed")
        self.temp_lbl = Label(self.mainFrame, font=("Arial", 22), bg="#202124")
        self.date = Label(self.mainFrame, font=("Arial", 12), bg="#202124", fg="#9aa0a6")
        self.details = Label(self.mainFrame, font=("Arial", 12), bg="#202124", fg="#e8eaed", anchor="e", justify=LEFT)
        
        self.titlebar.pack(expand=True, fill=X, anchor=N)
        self.search_etr.pack(side=LEFT, padx=10)
        self.search_btn.pack(side=LEFT) 
        self.close_btn.pack(side=RIGHT, padx=10) 

        self.mainFrame.pack(expand=True, fill=BOTH, anchor=N)
        self.locat_lbl.grid(row=0, column=0, padx=10)
        self.date.grid(row=0, column=1)
        self.icon.grid(row=1, column=0)
        self.weather_lbl.grid(row=2, column=0)
        self.temp_lbl.grid(row=1, column=1, sticky=S)
        self.details.grid(row=1, column=2, sticky=E)
    
    def create_icon(self, icon):
        # upload the icon
        raw_data = urlopen(f"http://openweathermap.org/img/wn/{icon}@2x.png").read()
        temp_img = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(temp_img)
        self.icon["image"] = image
        self.icon.image = image

    def search_city(self):
        # set city as argument for get_data
        self.get_data(city=self.search_etr.get())
        self.search_etr.delete(0, 'end')
    
    def get_data(self, city="Odessa"):
        # get information with api
        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        mode = "GET"
        querystring = {"q":{city},"lang":"en","units":"metric"}
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': API
        }
        try:
            response = requests.request(mode, url, headers=headers, params=querystring)
            response = response.json()
            self.render_data(response)
        except:
            messagebox.showerror("Error", f"The city <{city}> does not exist in our database")

    def set_color_by_temp(self, data):
        # setting the color (from darkblue as coldest to red as hottest) to temp_lbl
        temp = int(str(round(data['main']['feels_like'], 0))[:-2])
        if temp >= 30:
            self.temp_lbl["fg"] = "red"
        elif temp >= 20 and temp < 30:
            self.temp_lbl["fg"] = "orange"
        elif temp >= 10 and temp < 20:
            self.temp_lbl["fg"] = "yellow"
        elif temp < 10 and temp > 0:
            self.temp_lbl["fg"] = "lightblue"
        elif temp <= 0:
            self.temp_lbl["fg"] = "darkblue"
        return f'{temp} С\N{DEGREE SIGN}'

    def render_data(self, data):
        # display given data
        self.locat_lbl["text"] = f"{data['name']},{data['sys']['country']}"
        self.temp_lbl["text"] = f"{self.set_color_by_temp(data=data)}\n"
        self.weather_lbl["text"] = f"{data['weather'][0]['description'].capitalize()}"
        self.create_icon(data["weather"][0]["icon"])
        self.date["text"] = date.today().strftime("%b-%d-%Y")
        self.details["text"] = (f"Feels like: {str(round(data['main']['feels_like'], 0))[:-2]} С\N{DEGREE SIGN}\n"+
                               f"Wind: {data['wind']['speed']} km/h\n"+
                               f"Humidity: {data['main']['humidity']}%\n"+
                               f"Sunrise: {ctime(data['sys']['sunrise'])[11:-5]}\n"+
                               f"Sunset: {ctime(data['sys']['sunset'])[11:-5]}")