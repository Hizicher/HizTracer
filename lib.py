from PIL import Image
import os
from math import sqrt

# Vector class defines basic vector properties and operations
class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other): 
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

            raise ValueError(f"A vector may merely be divided by a scalar, so dividing with {other} does not work")

    def __mul__(self, other):

        try:

            new_x = self.x * other
            new_y = self.y * other
            new_z = self.z * other

            return Vector(new_x, new_y, new_z)

        except:

            raise ValueError(f"A vector may merely be multiplied with a scalar")

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

# Window class determines the FOV and image properties of the raytraced image
class Window:

    def __init__(self, size_x: int, size_y: int, name: str, color: Vector):

        self.size_x = size_x                                    # Width of the image
        self.size_y = size_y                                    # Height of the image
        self.name = name                                        # Image's name to be recorded inside /static
        self.aspect_ratio = float(self.size_x / self.size_y)    # This is calculated for defining y_min and y_max in the image
        self.color = color                                      # Backrgound color of the image (color of the sky)

        self.left_side = -1                                     # It is assumed that the left side has an x coordinate of -1 and right side has 1
        self.right_side = 1
        self.upside = -1 / self.aspect_ratio                    # Same logic for y but instead using aspect ratio
        self.downside = 1 / self.aspect_ratio

        self.x_step = (self.right_side - self.left_side) / (self.size_x - 1)    # Calculating how much x and y step it takes to proceed the next pixel
        self.y_step = (self.downside - self.upside) / ((self.size_y - 1))
         
        files = os.listdir("./static")                          # Opening the /static directory for seeing if an image with the same name is created, if yes, choose that image, else create a new one

        if  name not in files:

            self.filename = name
            
            self.img = Image.new("RGB", (size_x, size_y), color.as_tuple(True))
            self.img.save(f"static/{name}.png")

# Rays, that are being sent out from the "camera", is an instance of this class
class Ray:

    def __init__(self, origin: Vector, direction: Vector):

        self.origin = origin
        self.direction = direction.normalize()

# Material is for defining the reflectivity and specular constants of the shapes
class Material:

    def __init__(self, reflectivity, specular_constant):

        self.reflectivity = reflectivity
        self.specular_constant = specular_constant

# A parent class for class Wall and Sphere
class Shape:

    def __init__(self, color, material):

        self.color = color
        self.material = material

# Sphere class for defining the spheres, the class inherits the Shape class
class Sphere(Shape):

    def __init__(self, center: Vector, radius, color: Vector, material: Material):

        super().__init__(color=color, material=material)
        self.center = center
        self.radius = radius

# Lights are defined via this class,the reason both the color and position is a vector is because vectors' addition rules goes hand in hand with what we want to do on lights' attributes
class Light:

    def __init__(self, position: Vector, color: Vector):

        self.position = position
        self.color = color


class Wall(Shape): 

    # The user defines the corners of the wall, and then the program calculates vectors between these points to take the cross product for finding the normal of the wall to see it as a 3D plane.
    def __init__(self, left_upper_corner: Vector, left_lower_corner: Vector, right_upper_corner: Vector, right_lower_corner: Vector, color: Vector, material: Material):

        super().__init__(color=color, material=material)

        self.left_upper = left_upper_corner
        self.left_lower = left_lower_corner
        self.right_upper = right_upper_corner
        self.right_lower = right_lower_corner

        vector_1 = self.left_upper - self.left_lower
        vector_2 = self.right_upper - self.left_upper

        self.normal_vector = vector_1.cross_product(vector_2).normalize()
    
    # The calculations later on will be made assuming that the walls are 3D planes, but although the wall and the hit point might be on the same plane they of course do not have to intercept, which this method checks if they do
    def check_hit_point(self, point: Vector):
        
        error_margin = 1 / 1000
        x_min = min(self.left_upper.x, self.right_upper.x, self.left_lower.x, self.right_lower.x)
        x_max = max(self.left_upper.x, self.right_upper.x, self.left_lower.x, self.right_lower.x)

        y_min = min(self.left_upper.y, self.left_lower.y, self.right_upper.y, self.right_lower.y)
        y_max = max(self.left_upper.y, self.left_lower.y, self.right_upper.y, self.right_lower.y)

        z_min = min(self.left_upper.z, self.left_lower.z, self.right_upper.z, self.right_lower.z)
        z_max = max(self.left_upper.z, self.left_lower.z, self.right_upper.z, self.right_lower.z)

        return (y_min - error_margin <= point.y <= y_max + error_margin) and (x_min - error_margin <= point.x <= x_max + error_margin) and (z_min - error_margin <= point.z <= z_max + error_margin)

# The class where all the objects, lights and the window is assembled for rendering the wished raytraced image
class Scene:

    def __init__(self, window: Window, shapes: list, camera: Vector, lights: list, max_depth):

        self.window = window
        self.shapes = shapes
        self.camera = camera
        self.lights = lights
        self.progress = 0                   # In order to let the user know about the rendering progress this attribute keeps having a look over the process
        self.MAX_DEPTH = max_depth          # Determines the maximum amount of light bouncings to occur

    # Saves the changed pixels of the image object
    def blit_image(self):
        
        pixels = self.window.img.load()

        self.ray_trace_sphere(self.shapes, pixels)
    
        self.window.img.save(f"static/{self.window.name}.png")

    # Goes through every single pixel by also matching it with their coordinates
    def ray_trace_sphere(self, shapes: list, pixels):
        
        self.progress = 0
        screen_size = self.window.size_y * self.window.size_x

        for i in range(self.window.size_y):

            y = self.window.upside + self.window.y_step * i

            for j in range(self.window.size_x):
                
                x = self.window.left_side + self.window.x_step * j

                ray = Ray(self.camera, Vector(x, y, 0) - self.camera)

                color = self.ray_bounce(ray, shapes, 0) 

                pixels[j, i] = color.as_tuple(True)
                
                self.progress = 100 * (i  * self.window.size_x + j) // screen_size
                #print(f"{self.window.name}: {self.progress}", end="%\r")

        self.progress = 100
    
    # Recursively applying shading and reflection by calculating where the light will end up and what color the objects in the path of the light has
    def ray_bounce(self, ray: Ray, shapes: list, amount_of_calls: int):
        
        if amount_of_calls == self.MAX_DEPTH:               # Break if maximum amount of bounces is made

            return self.window.color
        
        hit_position, shape = self.closest_object(ray, shapes)  # Check first closest object to avoid choosing another object that the light hits after another
        
        if hit_position is None:

            return self.window.color                            # Return the background/sky color if there is no object that the light hit
        
        for light in self.lights:                               # To include the colors of the all lights present in the environment

            color_diffused = self.diffuse(shape, ray, hit_position, shape.color)            # Diffuse and shade colors
            color_specular_shaded = self.specular_shade(shape, ray, light, hit_position)

            color = color_diffused + color_specular_shaded
            
            if isinstance(shape, Sphere):               # Normal ray calculation differs, because a normal ray for a sphere is its radius vector while for wall it is the cross product of two present vectors on the wall

                normal_ray = hit_position - shape.center
            
            elif isinstance(shape, Wall):

                normal_ray = shape.normal_vector

            normal_ray = normal_ray.normalize()
            reflected_ray = Ray(hit_position + normal_ray * 1 / 1000 , self.reflect_ray(normal_ray, ray.direction).normalize()) # Reflect ray by using reflection law
            
            color += self.ray_bounce(reflected_ray, shapes, amount_of_calls + 1) # Recursion till the end
     
        return color
    

    def closest_object(self, ray: Ray, shapes: list):
        
        min_distance = -1
        min_shape = None
        hit_position = None

        for shape in shapes:

            if isinstance(shape, Sphere): # A sphere has the equation of x ** 2 + y ** 2 = r, and to calculate a potential intercept we are using the quadratic formula with some other parameters

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

                t = (shape.right_lower - ray.origin).dot_product(shape.normal_vector) / direction_and_normal        # For finding if a point is on a surface or not we can create a vector from a point on the wall to that point and see if that vector is orthogonal to the normal, and later on find the distance by this derived formula

                if t < 0:

                    continue
                
                hit_point = ray.origin + ray.direction * t

                if not shape.check_hit_point(hit_point): # See if the point and the plane intercepts with each other

                    continue

                distance = t

            if min_distance == -1:

                min_distance = distance
                min_shape = shape

                continue

            if distance < min_distance: # If a new smaller point is found, choose it

                min_distance = distance
                min_shape = shape

                continue

        if min_shape is not None:  # Checks if there is a shape hit or not

            hit_position = ray.origin + ray.direction * min_distance

            return hit_position, min_shape
        
        return None, None

    def reflect_ray(self, normal: Vector, incident: Vector):

        return incident - normal * 2 * incident.dot_product(normal) # Calculating the reflected vector
    
    def diffuse(self, shape: Shape, ray: Vector, hit_position, color: Vector):
        
        if isinstance(shape, Sphere):

            normal_vector = (shape.center - hit_position).normalize()

        elif isinstance(shape, Wall):

            normal_vector = shape.normal_vector

            if normal_vector.x < 0 or normal_vector.y < 0 or normal_vector.z < 0:

                normal_vector *= -1 # So that if the normal vector is negative the diffuse constant does not become negative
                
        return color * max(normal_vector.dot_product(ray.direction), 0)

    # Shades the colors by the reflection amount
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

