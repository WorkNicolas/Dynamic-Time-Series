import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as CanvasGraph
import threading
import time

# Model
class HumidityModel:
    def __init__(self, data):
        self.data = data
    
    def insert(self, value):
        self.data.append(value)
        with open("humidity_data.txt", "a") as file:
            file.write(f"{value}\n")
    
    def readDataRange(self, data_range):
        data_range_int = int(data_range)
        return self.data[data_range_int:data_range_int+6]
    
    def rotateArray(self):
        self.data = self.data[1:] + self.data[:1]

# View
class View:
    def __init__(self, root):
        # Root
        self.root = root
        self.root.title("Humidity Sensor Static Time Data Series")
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Stack 1
        self.input_frame = tk.Frame(root)
        self.input_frame.grid(row=0, column=0, sticky="ew")
        
        self.button_rotate_array = tk.Button(self.input_frame, text="Go", width=15)
        self.button_rotate_array.pack(side=tk.TOP)
        
        # Stack 2
        # Empty graph frame
        self.graph_frame = tk.Frame(root, bg="white", height=300, width=500)
        self.graph_frame.grid(row=1, column=0, sticky="nsew")
        
        # matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5,4))
        
        # Decorations
        self.ax.set_title("Humidity", loc="left")
        self.ax.set_xlim(0, 5)
        self.ax.set_ylim(0, 100)
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        
        # Draw
        self.canvas = CanvasGraph(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def bind_rotate_array(self, callback):
        self.button_rotate_array.config(command=lambda: callback())
    
    def update_plot(self, data_arr):
        # y axis
        range_data = list(range(1, len(data_arr)+1))
        self.ax.clear()
        
        # Decoration
        self.ax.set_title("Humidity", loc="left")
        
        # Line
        self.ax.plot(range_data, data_arr, color="red")
        
        # Bar
        self.ax.bar(range_data, data_arr, width=0.6, color="lightgreen", edgecolor="black")
        
        self.canvas.draw_idle()

# Controller
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Initial update
        self.go_update_plot(0)
        
        # Keep Running with GUI
        self.view.bind_rotate_array(self.keep_rotating)
    
    def keep_rotating(self):
        self.update_thread = threading.Thread(target=self.update_view_and_rotate_array)
        self.update_thread.start()
    
    def update_view_and_rotate_array(self):
        while True:
            # Update view then rotate
            update_view_thread = threading.Thread(target=self.go_update_plot, args=(0,))
            model_rotate_thread = threading.Thread(target=self.model.rotateArray)
            
            # Start Threads
            update_view_thread.start()
            time.sleep(0.1)
            model_rotate_thread.start()
            update_view_thread.join()
            model_rotate_thread.join()
            
            # Sleep
            time.sleep(1)
    
    def go_update_plot(self, data_range):
        print(f"Model Subset: {self.model.readDataRange(data_range)}")
        print(f"First Index: {self.model.readDataRange(data_range)[0]}")
        data_arr = self.model.readDataRange(data_range)
        self.view.update_plot(data_arr)

# Data Retrieval
def retrieveData():
    data = []
    with open("humidity_data.txt", "r") as file:
        for line in file:
            data.append(int(line.strip()))
    return data

# Main Execution
def main():
    root = tk.Tk()
    model = HumidityModel(retrieveData())
    view = View(root)
    controller = Controller(model, view)
    
    print(f"Model Data: {model.data}")
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
