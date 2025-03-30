"""
Group 1 Display Chart prepared by:
 - Carl Nicolas V. Mendoza | 301386435
 - Michael Asfeha          | 301411864
 - Ali Asjid Muhammad      | 301105070

"""
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as CanvasGraph
import threading
import time

class HumidityModel:
    def __init__(self, data):
        self.data_count = 0
        self.data = data
        
    def insert(self, value):
        self.data.append(value)
        with open("humidity_data.txt", "a") as file:
            file.write(f"{value}\n")
        
    def readDataCount(self):
        with open("humidity_data.txt") as file:
            for _ in file:
                self.data_count += 1
                
    def readDataRange(self, data_range):
        data_range_int = int(data_range)
        data_arr = []
        for i in range(data_range_int, data_range_int+5):
            if i < len(self.data):
                data_arr.append(self.data[i])
            else:
                break
        return [value for value in self.data[data_range_int:data_range_int+6] if data_range_int+6 <= len(self.data)]
    
    def rotateArray(self):
        self.data = self.data[1:] + self.data[:1]

class View:
    def __init__(self, root):
        # Root
        self.root = root
        self.root.title("Humidity Sensor Static Time Data Series")
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Stack 2
        # Empty graph frame
        self.graph_frame = tk.Frame(root, bg="white", height=300, width=500)
        self.graph_frame.grid(row=1, column=0, sticky="nsew")
        
        # matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5,4))
        
        self.ax.set_title(f"Data Range: Empty", loc="left")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.set_xlim(0, 5)
        self.ax.set_ylim(0, 100)
        for spine in self.ax.spines.values(): # Square Outline
            spine.set_visible(False)
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        
        self.line = self.ax.plot([], [], label="Humidity", color="green")
        
        self.canvas = CanvasGraph(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def update_plot(self, data_arr):
        # y axis
        range_data = list(range(1, len(data_arr)+1))
        self.ax.clear()
        
        # Decoration
        self.ax.set_title(f"Rotating Array", loc="left")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        
        # Line
        self.ax.plot(range_data, data_arr, label="", color="red")
        
        # Bar
        self.ax.bar(range_data, data_arr, width=0.6, color="lightgreen", edgecolor="black")
        
        self.canvas.draw_idle()

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Initial update
        self.go_update_plot(0)
        
        # Keep Running with GUI
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True  # Ensure thread terminates when main program exits
        self.update_thread.start()
        
    def update_loop(self):
        while True:
            # Update view then rotate
            update_view_thread = threading.Thread(target=self.go_update_plot, args=(0,))
            model_rotate_thread = threading.Thread(target=self.model.rotateArray)
            
            # Start Threads
            update_view_thread.start()
            model_rotate_thread.start()
            update_view_thread.join()
            model_rotate_thread.join()
            
            # Sleep
            time.sleep(0.5)
        
    def go_update_plot(self, data_range):
        print(f"Model Subset: {self.model.readDataRange(data_range)}")
        data_arr = self.model.readDataRange(data_range)
        self.view.update_plot(data_arr)

def readingTest():
    try:
        with open("humidity_data.txt", "r") as file:
            for line in file:
                print(line)
    except FileNotFoundError:
        print("Creating new humidity_data.txt file")
        with open("humidity_data.txt", "w") as file:
            for i in range(10):
                file.write(f"{i*10}\n")

def retrieveData():
    data = []
    try:
        with open("humidity_data.txt", "r") as file:
            for line in file:
                data.append(int(line.strip()))
    except FileNotFoundError:
        print("Creating new humidity_data.txt file")
        with open("humidity_data.txt", "w") as file:
            for i in range(10):
                file.write(f"{i*10}\n")
            data = [i*10 for i in range(10)]
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