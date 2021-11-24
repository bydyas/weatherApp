from tkinter import Tk
from source.weather_app import WeatherApp

def main(): 
    root = Tk()
    myApp = WeatherApp(root).get_data(city="Minsk")
    root.title("WeatherApp")
    root.geometry("450x450")
    root.resizable(False, False)
    root.configure(bg="blue")
    root.mainloop()

if __name__ == '__main__':
    main()