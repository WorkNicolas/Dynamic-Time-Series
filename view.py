# Imports
## GUI
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as CanvasGraph
## Style
from style import Style

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
        self.button_rotate_array.pack(side=tk.TOP, padx=Style.PADX, pady=Style.PADY)
        
        # Stack 2
        # Empty graph frame
        self.graph_frame = tk.Frame(root, bg="white", height=300, width=500)
        self.graph_frame.grid(row=1, column=0, sticky="nsew")
        
        # matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5,4))
        
        # Decorations
        self.ax.set_title(f"Data Range: Empty", loc="left")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.set_xlim(0, 5)
        self.ax.set_ylim(0, 100)
        for spine in self.ax.spines.values(): # Square Outline
            spine.set_visible(False)
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        self.line = self.ax.plot([], [], label="Humidity", color="green")
        
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
        self.ax.set_title(f"Humidity", loc="left")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        
        # Line
        self.ax.plot(range_data, data_arr, label="", color="red")
        
        # Bar
        self.ax.bar(range_data, data_arr, width=0.6, color="lightgreen", edgecolor="black")
        
        self.canvas.draw_idle()