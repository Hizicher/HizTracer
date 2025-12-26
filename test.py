import pytest
from lib import Vector

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




test_is_addition_working()
test_is_subtraction_working()
test_is_multiplication_working()
test_is_magnitude_correct()
test_is_normalization_working()
test_is_dot_product_working()