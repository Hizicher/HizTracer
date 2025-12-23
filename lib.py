class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    

    def __iadd__(self, other): # These methods are defining addition, multiplication and division with vectors, where division and multiplication ofcourse occurs with scalars

        self.x += other.x
        self.y += other.y 

        return self
    
    def __truediv__(self, other):
        new_x = self.x / other
        new_y = self.y / other

        return Vector(new_x, new_y)

    def __mul__(self, other):
        new_x = self.x * other
        new_y = self.y * other

        return Vector(new_x, new_y)
    

