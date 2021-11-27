from tkinter import Tk
from source.weather_app import WeatherApp

def main(): 
    root = Tk()
    app = WeatherApp(root).get_data()
    root.title("WeatherApp")
    root.resizable(False, False)
    root.configure(bg="#202124")
    # icon
    root.iconbitmap('source/icon.ico')
    # always on top
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    # center the window
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    x = (w / 2) - (450 / 2)
    y = (h / 2) - (410 / 2)
    root.geometry(f'{400}x{200}+{int(x)}+{int(y)}')
    
    root.mainloop()

if __name__ == '__main__':
    main()