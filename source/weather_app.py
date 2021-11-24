import requests
from tkinter import *
from tkinter import Tk, font
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen

class WeatherApp:
    def __init__(self, master: Tk):
        self.master = master
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=12, weight="bold")
        self.create_widgets()
        self.master.bind("<FocusIn>",self.deminimize_window) 

    def move_window(self,e):
        self.master.geometry(f'+{e.x_root}+{e.y_root}')
   
    def minimize_window(self):
        self.master.attributes("-alpha",0)
        self.master.minimized = True       

    def deminimize_window(self, event):
        self.master.focus() 
        self.master.attributes("-alpha",1)
        if  self.master.minimized == True:
            self.master.minimized = False   

    def create_widgets(self):
        # create modified titlebar
        self.master.overrideredirect(True)
        self.titlebar = Frame(self.master, bg="#202124", bd=0, relief="raised")
        self.titlebar.pack(expand=1, fill=X)
        # bind the titlebar
        self.titlebar.bind('<B1-Motion>', self.move_window)

        self.close_btn = Button(self.titlebar, text="  ×  ", bg="#202124", fg="#e8eaed", 
                                cursor="mouse", relief="sunken", bd=0, command=self.master.quit)
        self.minimize_btn = Button(self.titlebar, text=' ߺ ', bg="#202124", fg="#e8eaed", 
                                cursor="mouse", relief="sunken", bd=0, command=self.minimize_window)

        self.search_etr = Entry(self.titlebar, bg="#e8eaed", bd=0)
        self.search_btn = Button(self.titlebar, text="Search", bg="#202124", fg="#e8eaed", 
                                cursor="mouse", relief="sunken", bd=0, command=self.search_city)
        
        self.locat_lbl = Label(self.master, font=("Arial", 22), bg="#202124", fg="#e8eaed")
        self.temp_lbl = Label(self.master, font=("Arial", 22), bg="#202124", fg="#e8eaed")
        self.weather_lbl = Label(self.master, bg="#202124", fg="#e8eaed")
        self.icon = Label(self.master, bg="#202124")
        
        self.search_etr.pack(side=LEFT, padx=10) # search bar
        self.search_btn.pack(side=LEFT) # search btn
        self.close_btn.pack(side=RIGHT, padx=10) # close btn
        self.minimize_btn.pack(side=RIGHT, pady=2) 

        self.locat_lbl.pack() # city
        self.icon.pack()
        self.temp_lbl.pack() # real temp
        self.weather_lbl.pack() # description
    
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
            'x-rapidapi-key': "32c4ac93d2msh32e94c84194df3fp166d6ajsnec3e473f2c4e"
        }

        response = requests.request(mode, url, headers=headers, params=querystring)
        response = response.json()
        self.render_data(response)

    def render_data(self, data):
        # display given data
        self.locat_lbl["text"] = f"{data['name']},{data['sys']['country']}"
        self.temp_lbl["text"] = f"{str(round(data['main']['temp'], 0))[:-2]} С\N{DEGREE SIGN}\n"
        self.weather_lbl["text"] = f"{data['weather'][0]['description'].capitalize()}"
        self.create_icon(data["weather"][0]["icon"])