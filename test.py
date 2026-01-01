import pytest
from lib import Vector, Window, Ray, Sphere, Scene, Light, Material
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

    window = Window(540, 400, "test-1")
    material = Material(0.5, 32)
    red_sphere = Sphere(Vector(0, -0.4, 0), 0.1, Vector(255, 0, 0), material)
    yellow_sphere = Sphere(Vector(0, 0, 0), 0.1, Vector(0, 255, 255), material)
    green_sphere = Sphere(Vector(0, 0.4, 0), 0.1, Vector(0, 255, 0), material)
    light = Light(Vector(1, window.upside, 0), Vector(255, 255, 255))
    objects = [red_sphere, yellow_sphere, green_sphere]
    camera = Vector(0, 0, -1)
    scene = Scene(window, objects, camera, light, 0, 3)
    scene.blit_image()


def test_render_with_reflections():

    window = Window(540, 400, "test-2")
    material = Material(0.5, 32)
    blue_sphere = Sphere(Vector(0.75, -0.1, 1), 0.6, Vector(0, 0, 255), material)
    pink_sphere = Sphere(Vector(-0.75, -0.1, 2.25), 0.6, Vector(125, 80, 125), material)
    ground_sphere = Sphere(Vector(0, 1000.5, 1), 1000, Vector(0, 175, 0), material)
    light = Light(Vector(1, window.upside, 0), Vector(255, 255, 255))
    objects = [blue_sphere, pink_sphere, ground_sphere]
    camera = Vector(0, -0.35, -1)
    scene = Scene(window, objects, camera, light, 0, 8)
    scene.blit_image()




test_is_addition_working()
test_is_subtraction_working()
test_is_multiplication_working()
test_is_magnitude_correct()
test_is_normalization_working()
test_is_dot_product_working()
#test_render()
test_render_with_reflections()