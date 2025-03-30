# Imports
## GUI
import tkinter as tk
from tkinter import ttk
## MVC
from model import HumidityModel
from view import View
from controller import Controller

def readingTest():
    # FIXED: VSCode is opened in static_time_data_series/
    # and is getting stuff there instead of humidity_data.txt 
    # from static_time_data_series/lab/
    with open("humidity_data.txt", "r") as file:
        for line in file:
            print(line)

def retrieveData():
    data = []
    with open("humidity_data.txt", "r") as file:
        for line in file:
            data.append(int(line.strip()))
    return data

def main():
    readingTest()
    root = tk.Tk()
    model = HumidityModel(retrieveData())
    view = View(root)
    controller = Controller(model, view)
    print(f"Model Data: {model.data}")
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
    