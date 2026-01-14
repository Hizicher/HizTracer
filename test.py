import pytest
from lib import Vector, Window, Ray, Sphere, Scene, Light, Material, Wall
from PIL import Image

def test_is_addition_working():

    vector_a = Vector(1, 2 , 3)
    vector_b = Vector(4, 5, 6)
    vector_c = vector_a + vector_b

    assert vector_c.x == 5 and vector_c.y == 7 and vector_c.z == 9

def test_is_subtraction_working():

    vector_a = Vector(1, 2 , 3)
    vector_b = Vector(4, 2, 8)
    vector_c = vector_a - vector_b

    assert vector_c.x == -3 and vector_c.y == 0 and vector_c.z == -5


def test_is_multiplication_working():

    vector_a = Vector(1, 2 , 3)
    vector_b = vector_a * 10

    assert vector_b.x == 10 and vector_b.y == 20 and vector_b.z == 30


def test_is_magnitude_correct():

    vector_a = Vector(3, 4, 0)

    assert vector_a.magnitude() == 5.0

def test_is_normalization_working():

    vector_a = Vector(3, 4, 0)

    vector_b = vector_a.normalize()

    assert vector_b.x == 3 / 5 and vector_b.y == 4 / 5 and vector_b.z == 0

def test_is_dot_product_working():

    vector_a = Vector(3, 4, 0)
    vector_b = Vector(1, 2, 5)
    product = vector_a.dot_product(vector_b)

    assert product == 11

def test_render():

    window = Window(540, 400, "test-1", Vector(0, 0, 0))
    material = Material(0.5, 32)
    red_sphere = Sphere(Vector(0, -0.4, 0), 0.1, Vector(255, 0, 0), material)
    yellow_sphere = Sphere(Vector(0, 0, 0), 0.1, Vector(0, 255, 255), material)
    green_sphere = Sphere(Vector(0, 0.4, 0), 0.1, Vector(0, 255, 0), material)
    lights = [Light(Vector(1, window.upside, 0), Vector(255, 255, 255))]
    objects = [red_sphere, yellow_sphere, green_sphere]
    camera = Vector(0, 0, -1)
    scene = Scene(window, objects, camera, lights, 3)
    scene.blit_image()


def test_render_with_reflections_and_walls():

    window = Window(540, 400, "test-3", Vector(0, 0, 0))

    material = Material(0.5, 32)
    mat_wall_matte = Material(0, 8)     
    mat_wall_semi = Material(0.3, 32) 
    mat_wall_mirror = Material(0.7, 64)

    black_wall = Wall(Vector(-3,  2, 4), Vector(-3,  -2, 4), Vector(3, 2, 4), Vector(3, -2, 4), Vector(0, 0, 200), mat_wall_matte)
    left_wall = Wall(Vector(-3,  2, 4), Vector(-3,  -2, 4), Vector(-3, 2, 0), Vector(-3, -2, 0), Vector(255, 80, 80), mat_wall_semi)
    right_wall = Wall(Vector(3,  2, 0), Vector(3,  -2, 0), Vector(3, 2, 4), Vector(3, -2, 4), Vector(200, 200, 200), mat_wall_mirror)
    floor_wall = Wall(Vector(-3,  0.5, 0), Vector(-3,  0.5, 4), Vector(3, 0.5, 0), Vector(3, 0.5, 4), Vector(120, 120, 120), mat_wall_matte)

    blue_sphere = Sphere(Vector(0.75, -0.1, 1), 0.6, Vector(0, 0, 255), material)
    pink_sphere = Sphere(Vector(-0.75, -0.1, 2), 0.6, Vector(125, 80, 125), material)
    
    lights = [Light(Vector(1, window.upside, 0), Vector(255, 255, 255)), Light(Vector(-0.5, -0.5, 0), Vector(255, 255, 255))]
    objects = [blue_sphere, pink_sphere, black_wall, left_wall, right_wall, floor_wall]
    camera = Vector(0, 0, -1)
    scene = Scene(window, objects, camera, lights, 8)
    scene.blit_image()



def test_one_ball_one_wall():

    window = Window(540, 400, "test-5", Vector(0, 0, 0))

    material = Material(0.5, 32)
    mat_wall_matte = Material(0, 8)     

    floor_wall = Wall(Vector(-3,  0.5, 0), Vector(-3,  0.5, 4), Vector(3, 0.5, 0), Vector(3, 0.5, 4), Vector(120, 120, 120), mat_wall_matte)

    blue_sphere = Sphere(Vector(0.75, -0.1, 1), 0.6, Vector(0, 0, 255), material)
    
    lights = [Light(Vector(-0.5, -0.5, 0), Vector(255, 255, 255))]
    objects = [blue_sphere, floor_wall]
    camera = Vector(0, 0, -1)
    scene = Scene(window, objects, camera, lights, 8)
    scene.blit_image()


test_is_addition_working()
test_is_subtraction_working()
test_is_multiplication_working()
test_is_magnitude_correct()
test_is_normalization_working()
test_is_dot_product_working()
test_render()
test_render_with_reflections_and_walls()
test_one_ball_one_wall()