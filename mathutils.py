PI = 3.1415926535
INF = float('inf')

class Vector3:
    def __init__(self, x:float=0, y:float=0,z:float=0):
        self.x = x
        self.y = y
        self.z = z

    def norm(self):
        return (self.x ** 2 + self.y **2 + self.z ** 2)**0.5

    def normalize(self):
        return self * (1 /  self.norm())

    def __add__(self, other):
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)
            
    def __radd__(self, other):
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)

    def __sub__(self, other):
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z)
    
    def __rsub__(self, other):
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z)

    def __mul__(self, other:int|float):
        return Vector3(
                    self.x * other,
                    self.y * other,
                    self.z * other)
    
    def dot(self, other):
        return self.x*other.x + self.y * other.y + self.z * other.z

    def __matmul__(self, other):
        return self.dot(other)

    def __invert__(self):
        return self.normalize()

    def __repr__(self):
        return f"<Vector3({self.x} {self.y} {self.z})>"


