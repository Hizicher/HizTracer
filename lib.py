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
    def add_tuples_and_vectors(self, other: tuple):

        return round(other[0] + self.x), round(other[1] + self.y), round(other[2] + self.z)

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

class Material:

    def __init__(self, reflectivity, specular_constant):

        self.reflectivity = reflectivity
        self.specular_constant = specular_constant

class Sphere:

    def __init__(self, center: Vector, radius, color: Vector, material: Material):

        self.center = center
        self.radius = radius
        self.color = color
        self.material = material

class Light:

    def __init__(self, position: Vector, color: Vector):

        self.position = position
        self.color = color


class Scene:

    def __init__(self, window: Window, shapes: list, camera: Vector, light: Light, size, max_depth):

        self.window = window
        self.shapes = shapes
        self.size = size
        self.camera = camera
        self.light = light
        self.MAX_DEPTH = max_depth

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

                color = self.ray_bounce(j, i, ray, shapes, self.light.color, pixels, 0)
                pixels[j, i] = color.as_tuple(True)
                
                print(f"{100 * (i  * self.window.size_x + j) // screen_size}", end="%\r")
    
    def ray_bounce(self, j: int, i: int, ray: Ray, shapes: list, light_color: Vector, pixels, amount_of_calls: int):

        if amount_of_calls == self.MAX_DEPTH:

            return Vector(0, 0, 0)
        
        hit_position, shape = self.closest_object(ray, shapes)
        
        if not hit_position is None:

            color_diffused = self.diffuse_sphere(shape, ray, hit_position, shape.color)
            color_specular_shaded = self.specular_shading_sphere(shape, ray, hit_position, light_color)

            local_color = color_diffused + color_specular_shaded

            color_final = shape.color + color_diffused + color_specular_shaded

            normal_ray = hit_position - shape.center
            normal_ray = normal_ray.normalize()
            reflected_ray = Ray(hit_position + normal_ray, self.reflect_ray(normal_ray, ray.direction).normalize())
            
            return (local_color * (1 - shape.material.reflectivity) + self.ray_bounce(j, i, reflected_ray, shapes, color_final, pixels, amount_of_calls + 1) * shape.material.reflectivity)
                
        return Vector(0, 0, 0)
    

    def closest_object(self, ray: Ray, shapes: list):
        
        min_distance = -1
        min_shape = None

        for shape in shapes:

            sphere_to_ray = ray.origin - shape.center
            b = 2 * ray.direction.dot_product(sphere_to_ray)
            c = sphere_to_ray.dot_product(sphere_to_ray) - shape.radius ** 2
            discriminant = b ** 2 - 4 * c

            if discriminant >= 0:

                distance = (-b - sqrt(discriminant)) / 2

                if min_distance == -1:
    
                    min_distance = distance
                    min_shape = shape
                    continue

                if distance < min_distance and distance > 0:

                    min_distance = distance
                    min_shape = shape

        if min_shape != None:

            hit_position = ray.origin + ray.direction * min_distance

            return hit_position, min_shape
        
        return None, None


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
        blinn_term = halfway_vector.dot_product(reflected) ** shape.material.specular_constant

        return color * blinn_term

