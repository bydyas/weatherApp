from tkinter import Tk
from source.weather_app import WeatherApp

def main(): 
    root = Tk()
    myApp = WeatherApp(root).get_data()
    root.title("WeatherApp")
    root.resizable(False, False)
    root.configure(bg="#202124")
    # center the window
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    x = (w / 2) - (450 / 2)
    y = (h / 2) - (410 / 2)
    root.geometry(f'{400}x{200}+{int(x)}+{int(y)}')
 
    root.mainloop()

if __name__ == '__main__':
    main()