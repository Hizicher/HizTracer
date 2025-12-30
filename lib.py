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
    
    def as_tuple(self, rounded: bool):

        if rounded:

            return round(self.x), round(self.y), round(self.z)
        
        return self.x, self.y, self.z

    def multiply_colors(self, other):

        return Vector(round(255 * self.x / 255 * other.x / 255), round(255 * self.y / 255 * other.y / 255), round(255 * self.z / 255 * other.z / 255))

class Window:

    def __init__(self, size_x: int, size_y: int, name: str):

        self.size_x = size_x
        self.size_y = size_y
        self.name = name
        self.aspect_ratio = float(self.size_x / self.size_y)

        self.left_side = -1
        self.right_side = 1
        self.upside = -1 / self.aspect_ratio
        self.downside = 1 / self.aspect_ratio

        self.x_step = (self.right_side - self.left_side) / (self.size_x - 1)
        self.y_step = (self.downside - self.upside) / ((self.size_y - 1))
         
        files = os.listdir("./static")

        if  name not in files:

            self.filename = name
            
            self.img = Image.new("RGB", (size_x, size_y), (0, 0, 0))
            self.img.save(f"static/{name}.png")

class Ray:

    def __init__(self, origin: Vector, direction: Vector):

        self.origin = origin
        self.direction = direction.normalize()

class Sphere:

    def __init__(self, center: Vector, radius, color: Vector, material: str):

        self.center = center
        self.radius = radius
        self.color = color
        self.material = material

class Light:

    def __init__(self, position: Vector, color: Vector):

        self.position = position
        self.color = color


class Scene:

    def __init__(self, window: Window, shapes: list, camera: Vector, light: Light, size):

        self.window = window
        self.shapes = shapes
        self.size = size
        self.camera = camera
        self.light = light

    def blit_image(self):
        
        pixels = self.window.img.load()

        self.ray_trace_sphere(self.shapes, pixels)
    
        self.window.img.save(f"static/{self.window.name}.png")

    def ray_trace_sphere(self, shapes: list, pixels):
        
        screen_size = self.window.size_y * self.window.size_x

        for i in range(self.window.size_y):

            y = self.window.upside + self.window.y_step * i

            for j in range(self.window.size_x):
                
                x = self.window.left_side + self.window.x_step * j

                ray = Ray(self.camera, Vector(x, y, 0) - self.camera)

                self.ray_bounce(j, i, ray, shapes, self.light.color, pixels, 0)
                
                print(f"{100 * (i  * self.window.size_x + j) // screen_size}", end="%\r")
    
    def ray_bounce(self, j: int, i: int, ray: Ray, shapes: list, light_color: Vector, pixels, reflected_colors: list, amount_of_calls: int):

        if amount_of_calls == 3:

            pixels[j, i] = pixels[j, i][0] // 3, pixels[j, i][1] // 3, pixels[j, i][2] // 3

            return True
        
        for shape in shapes:

            distance = self.does_ray_hit(ray, shape)

            if distance != None and distance > 0:

                hit_position = ray.origin + ray.direction * distance

                color_diffused = self.diffuse_sphere(shape, ray, hit_position, shape.color)
                color_specular_shaded = self.specular_shading_sphere(shape, ray, hit_position, light_color)

                color_final = shape.color * 0 + color_diffused + color_specular_shaded
                color_final = shape.color.multiply_colors(color_final)
                reflected_colors.append(color_final)
                
                normal_ray = hit_position - shape.center
                normal_ray = normal_ray.normalize()
                ray_normalized = ray.normalize() * -1
                reflected_ray = self.reflect_ray(normal_ray, ray_normalized).normalize()

                self.ray_bounce(j, i, reflected_ray, shapes, color_final, pixels, reflected_colors, amount_of_calls + 1)

        if amount_of_calls > 1:

            pixels[j, i] = pixels[j, i][0] // amount_of_calls, pixels[j, i][1] // amount_of_calls, pixels[j, i][2] // 3
        
        return True
    
    def does_ray_hit(self, ray: Ray, shape: Sphere):

        sphere_to_ray = self.camera - shape.center
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - shape.radius ** 2
        discriminant = b ** 2 - 4 * c

        if discriminant >= 0:

            return (-b - sqrt(discriminant)) / 2
        
        return None

    def reflect_ray(self, normal: Vector, incident: Vector):

        return incident - normal * 2 * incident.dot_product(normal)
    
    def diffuse_sphere(self, shape: Sphere, ray: Vector, hit_position, color: Vector):
        
        normal_vector = shape.center - hit_position

        return color * normal_vector.normalize().dot_product(ray.direction)

    def specular_shading_sphere(self, shape: Sphere, ray: Vector, hit_position, color: Vector):
        
        normal_vector = shape.center - hit_position
        light_to_plane = hit_position - self.light.position
        viewer_vector = self.camera - hit_position

        normal_vector = normal_vector.normalize()
        light_to_plane = light_to_plane.normalize()
        viewer_vector = viewer_vector.normalize()

        reflected = self.reflect_ray(normal_vector, light_to_plane)
        light_to_plane *= -1
        halfway_vector = (light_to_plane + viewer_vector).normalize()
        blinn_term = halfway_vector.dot_product(reflected) ** 32

        return color * blinn_term

