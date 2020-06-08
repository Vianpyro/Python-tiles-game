from random import randint
from os import path

class Map:
    def __init__(self, width, height, details=1, minID=0, maxID=1, preferedID=None):
        self.width = max(2, width)
        self.height = max(2, height)
        if details < 0 or details // 1.5 > minID + maxID: self.details = minID + maxID // 2
        else: self.details = details
        if minID > maxID: self.minID, self.maxID = maxID, minID
        else: self.minID, self.maxID = minID, maxID
        if preferedID and minID <= preferedID <= maxID: self.prefID = preferedID
        else: self.prefID = None

    def new_line(self, width):
        if self.prefID: array = [self.prefID]
        else: array = [randint(self.minID, self.maxID)]
        for i in range (width - 1):
            value = randint(array[-1] - self.details, array[-1] + self.details)
            while value < self.minID or value > self.maxID:
                value = randint(array[-1] - self.details, array[-1] + self.details)
            array.append(value)
        return array

    def generate_2d_noise(self):
        return [self.new_line(self.width) for i in range (self.height)]

    def save_to_file(self, array, smooth=False, world_borders=False, wallsID=1, separator='', replace_zero_with=''):
        if smooth: self.smooth(array)
        if world_borders:
            world_borders_array = [wallsID for i in range (len(array[0]))]
            array[0] = array[-1] = world_borders_array
            for i in range (len(array)):
                array[i][0] = array[i][-1] = wallsID
        folder = path.dirname(__file__)
        with open(path.join(folder, 'save.wia'), 'w') as f:
            for line in array:
                for value in line:
                    if value == 0 and replace_zero_with != '': f.write(str(replace_zero_with) + separator)
                    else: f.write(str(value) + separator)
                f.write('\n')
            f.close()
    
    def smooth(self, array):
        for line in range (1, len(array)):
            for index, value in enumerate (array[line]):
                if value - (self.details * 2) >= array[line - 1][index]:
                    array[line][index] -= (self.details * 2)
                if value + (self.details * 2) <= array[line - 1][index]:
                    array[line][index] += (self.details * 2)
        return array
