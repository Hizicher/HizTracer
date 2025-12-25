from PIL import Image
import os

class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    

    def __iadd__(self, other): # These methods are defining addition, multiplication and division with vectors, where division and multiplication ofcourse occurs with scalars

        self.x += other.x
        self.y += other.y
        self.z += other.z 

        return self
    
    def __truediv__(self, other):
        new_x = self.x / other
        new_y = self.y / other
        new_z = self.z / other

        return Vector(new_x, new_y, new_z)

    def __mul__(self, other):
        new_x = self.x * other
        new_y = self.y * other
        new_z = self.z * other

        return Vector(new_x, new_y, new_z)
    
class Window:

    def __init__(self, size_x, size_y):
        

def blit_image():

    pass