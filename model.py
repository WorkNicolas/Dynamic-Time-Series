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
                break;
        return [value for value in self.data[data_range_int:data_range_int+6]]
    
    def rotateArray(self):
        self.data = self.data[1:] + self.data[:1]
