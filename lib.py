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
    
    def cross_product(self, other):

        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

class Window:

    def __init__(self, size_x: int, size_y: int, name: str, color: tuple):

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
            
            self.img = Image.new("RGB", (size_x, size_y), color)
            self.img.save(f"static/{name}.png")

class Ray:

    def __init__(self, origin: Vector, direction: Vector):

        self.origin = origin
        self.direction = direction.normalize()

class Material:

    def __init__(self, reflectivity, specular_constant):

        self.reflectivity = reflectivity
        self.specular_constant = specular_constant

class Shape:

    pass

class Sphere(Shape):

    def __init__(self, center: Vector, radius, color: Vector, material: Material):

        self.center = center
        self.radius = radius
        self.color = color
        self.material = material

    def __str__(self):

        return f'center = {self.center}'

class Light:

    def __init__(self, position: Vector, color: Vector):

        self.position = position
        self.color = color

class Wall(Shape): 

    def __init__(self, left_upper_corner: Vector, left_lower_corner: Vector, right_upper_corner: Vector, right_lower_corner: Vector, color: Vector, material: Material):

        self.left_upper = left_upper_corner
        self.left_lower = left_lower_corner
        self.right_upper = right_upper_corner
        self.right_lower = right_lower_corner

        self.color = color
        self.material = material

        vector_1 = self.left_upper - self.left_lower
        vector_2 = self.right_upper - self.left_upper

        self.normal_vector = vector_1.cross_product(vector_2).normalize()
        
    def check_hit_point(self, point: Vector):
        
        error_margin = 1 / 1000
        x_min = min(self.left_upper.x, self.right_upper.x, self.left_lower.x, self.right_lower.x)
        x_max = max(self.left_upper.x, self.right_upper.x, self.left_lower.x, self.right_lower.x)

        y_min = min(self.left_upper.y, self.left_lower.y, self.right_upper.y, self.right_lower.y)
        y_max = max(self.left_upper.y, self.left_lower.y, self.right_upper.y, self.right_lower.y)

        z_min = min(self.left_upper.z, self.left_lower.z, self.right_upper.z, self.right_lower.z)
        z_max = max(self.left_upper.z, self.left_lower.z, self.right_upper.z, self.right_lower.z)

        return (y_min - error_margin <= point.y <= y_max + error_margin) and (x_min - error_margin <= point.x <= x_max + error_margin) and (z_min - error_margin <= point.z <= z_max + error_margin)
    
class Scene:

    def __init__(self, window: Window, shapes: list, camera: Vector, lights: list, size, max_depth):

        self.window = window
        self.shapes = shapes
        self.size = size
        self.camera = camera
        self.lights = lights
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

                color = self.ray_bounce(ray, shapes, 0)

                pixels[j, i] = color.as_tuple(True)
                
                print(f"{self.window.name}: {100 * (i  * self.window.size_x + j) // screen_size}", end="%\r")
    
    def ray_bounce(self, ray: Ray, shapes: list, amount_of_calls: int):
        
        if amount_of_calls == self.MAX_DEPTH:

            return Vector(0, 0, 0)
        
        hit_position, shape = self.closest_object(ray, shapes)
        
        if hit_position is None:

            return Vector(0, 0, 0)
        
        for light in self.lights:

            color_diffused = self.diffuse(shape, ray, hit_position, shape.color)
            color_specular_shaded = self.specular_shade(shape, ray, light, hit_position)

            color = color_diffused + color_specular_shaded
            
            if isinstance(shape, Sphere):

                normal_ray = hit_position - shape.center
            
            elif isinstance(shape, Wall):

                normal_ray = shape.normal_vector

            normal_ray = normal_ray.normalize()
            reflected_ray = Ray(hit_position + normal_ray * 1 / 1000 , self.reflect_ray(normal_ray, ray.direction).normalize())
            
            color += self.ray_bounce(reflected_ray, shapes, amount_of_calls + 1)
     
        return color
    

    def closest_object(self, ray: Ray, shapes: list):
        
        min_distance = -1
        min_shape = None
        hit_position = None

        for shape in shapes:

            if isinstance(shape, Sphere):

                sphere_to_ray = ray.origin - shape.center
                b = 2 * ray.direction.dot_product(sphere_to_ray)
                c = sphere_to_ray.dot_product(sphere_to_ray) - shape.radius ** 2
                discriminant = b ** 2 - 4 * c

                if discriminant < 0:

                    continue

                distance = (-b - sqrt(discriminant)) / 2

                if distance < 0:

                    continue

            elif isinstance(shape, Wall):
                
                
                direction_and_normal = ray.direction.dot_product(shape.normal_vector)


                if direction_and_normal == 0:

                    continue

                t = (shape.right_lower - ray.origin).dot_product(shape.normal_vector) / direction_and_normal

                if t < 0:

                    continue
                
                hit_point = ray.origin + ray.direction * t

                if not shape.check_hit_point(hit_point):

                    continue

                distance = t

            if min_distance == -1:

                min_distance = distance
                min_shape = shape

                continue

            if distance < min_distance:

                min_distance = distance
                min_shape = shape

                continue

        if min_shape is not None:

            hit_position = ray.origin + ray.direction * min_distance

            return hit_position, min_shape
        
        return None, None

    def reflect_ray(self, normal: Vector, incident: Vector):

        return incident - normal * 2 * incident.dot_product(normal)
    
    def diffuse(self, shape: Shape, ray: Vector, hit_position, color: Vector):
        
        if isinstance(shape, Sphere):

            normal_vector = (shape.center - hit_position).normalize()

        elif isinstance(shape, Wall):

            normal_vector = shape.normal_vector

            if normal_vector.x < 0 or normal_vector.y < 0 or normal_vector.z < 0:

                normal_vector *= -1
                
        return color * max(normal_vector.dot_product(ray.direction), 0)

    def specular_shade(self, shape: Sphere, ray: Vector, light: Light, hit_position):

        if isinstance(shape, Sphere):

            normal_vector = shape.center - hit_position

        elif isinstance(shape, Wall):

            normal_vector = shape.normal_vector

        light_to_plane = hit_position - light.position
        viewer_vector = self.camera - hit_position

        normal_vector = normal_vector.normalize()
        light_to_plane = light_to_plane.normalize()
        viewer_vector = viewer_vector.normalize()

        reflected = self.reflect_ray(normal_vector, light_to_plane)
        light_to_plane *= -1
        halfway_vector = (light_to_plane + viewer_vector).normalize()
        blinn_term = max(halfway_vector.dot_product(reflected), 0) ** shape.material.specular_constant
    
        return light.color * blinn_term

