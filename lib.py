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

        self.size_x = size_x
        self.size_y = size_y
        self.aspect_ratio = float(self.size_x / self.size_y)

        self.left_side = - 1
        self.right_side = 1
        self.upside = -1 / self.aspect_ratio
        self.downside = 1 / self.aspect_ratio

        self.x_step = (self.right_side - self.left_side) / (self.size_x - 1)
        self.y_step = (self.downside - self.upside) / ((self.size_y - 1) * self.aspect_ratio) 


        files = os.listdir("./static")

        if  name not in files:

            self.filename = name
            
            self.img = Image.new("RGB", (size_x, size_y), (0, 0, 0))
            self.img.save(f"static/{name}.png")

    def coordinate_translator(self, point: Vector, pillow_to_real: bool):

        half_width = self.size_x / 2
        half_height = self.size_y / 2

        if pillow_to_real:

            return Vector((point.x - half_width) / (half_width) , (point.y + half_height) / (half_height * self.aspect_ratio)) 
        
        return Vector((point.x + half_width) / (half_width) , (point.y - half_height) / (half_height * self.aspect_ratio))

class Ray:

    def __init__(self, origin: Vector, direction: Vector):

        self.origin = origin
        self.direction = direction.normalize()

class Sphere:

    def __init__(self, center: Vector, radius):

        self.center = center
        self.radius = radius


class Scene:

    def __init__(self, window: Window, shapes: list, camera: Vector, size):

        self.window = window
        self.shapes = shapes
        self.size = size
        self.camera = camera

    def blit_image(self):

        for shape in self.shapes:

            if isinstance(shape, Sphere):

                for i in range(self.window.size_y):

                    y = self.window.upside + self.window.y_step * i

                    for j in range(self.window.size_x):
                        
                        x = self.window.left_side + self.window.x_step * j
                        sphere_to_ray = self.camera - shape.center
                        ray = Ray(self.camera, Vector(x, y, 0) - self.camera)

                        b = 2 * ray.direction.dot_product(sphere_to_ray)
                        c = sphere_to_ray.dot_product(sphere_to_ray) - shape.center ** 2
                        discriminant = b ** 2 - 4 * c
                        distance = (-b - discriminant) / 2