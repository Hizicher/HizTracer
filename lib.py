from PIL import Image
import os
from math import sqrt

class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other): # These methods are defining addition, multiplication and division with vectors, where division and multiplication ofcourse occurs with scalars

        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)


    def __sub__(self, other):

        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __truediv__(self, other):
        try:
            new_x = self.x / other
            new_y = self.y / other
            new_z = self.z / other

            return Vector(new_x, new_y, new_z)
        
        except:

            raise ValueError("A vector may merely be divided by a scalar")

    def __mul__(self, other):
        try:
            new_x = self.x * other
            new_y = self.y * other
            new_z = self.z * other

            return Vector(new_x, new_y, new_z)

        except:

            raise ValueError("A vector may merely be multiplied with a scalar")

    def magnitude(self):

        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):

        magnitude = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

        return self / magnitude
    
    def dot_product(self, other):

        return self. x * other.x + self.y * other.y + self.z * other.z
class Window:

    def __init__(self, size_x: int, size_y: int, name: str):

        files = os.listdir("./static")

        if  name not in files:

            self.filename = name
            
            self.img = Image.new("RGB", (size_x, size_y), (0, 0, 0))
            self.img.save(f"static/{name}.png")

def blit_image():

    pass