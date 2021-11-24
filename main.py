from tkinter import Tk
from source.weather_app import WeatherApp

def main(): 
    root = Tk()
    myApp = WeatherApp(root).get_data()
    root.title("WeatherApp")
    root.geometry("420x280")
    root.resizable(False, False)
    root.configure(bg="#202124")
    root.mainloop()

if __name__ == '__main__':
    main()