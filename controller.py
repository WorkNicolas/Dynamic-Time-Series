from model import HumidityModel
from view import View
import threading
import time

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
            time.sleep(0.4) # 0.1 + 0.4 = 0.5; Sometimes some parts are being skipped so that's why I did this
        
    def go_update_plot(self, data_range):
        print(f"Model Subset: {self.model.readDataRange(data_range)}")
        print(f"First Index: {self.model.readDataRange(data_range)[0]}")
        data_arr = self.model.readDataRange(data_range)
        self.view.update_plot(data_arr)