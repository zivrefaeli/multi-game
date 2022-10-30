from math import cos, sin, radians, sqrt

from .constants import *
from .methods import Methods

class Vector:
    def __init__(self, size: float = 0, angle: int = 0) -> None:
        self.size = size
        self.angle = angle

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value: float):
        self._size = round(value, ROUND_NUMBERS)

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, value: int):
        self._angle = (value + 360) % 360

    def get(self) -> tuple:
        dx = self.size * cos(radians(self.angle))
        dy = self.size * sin(radians(self.angle))
        return dx, dy

    def __add__(self, other):
        if type(other) != Vector:
            return None
        dx1, dy1 = self.get()
        dx2, dy2 = other.get()
        dx = dx1 + dx2
        dy = dy1 + dy2
        
        size = sqrt(dx ** 2 + dy ** 2)
        angle = Methods.get_angle_by_delta(dx, dy)
        return Vector(size, angle)

    def __str__(self) -> str:
        return f'Vector(|{self.size}|, {self.angle}°)'

if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')