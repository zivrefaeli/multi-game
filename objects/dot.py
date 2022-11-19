from math import sqrt, cos, sin, atan, degrees, radians, floor
from typing_extensions import Self
from .constants import ROUND_NUMBERS, WIDTH, HEIGHT


class Dot:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    @property
    def x(self) -> float:
        return self._x
    
    @x.setter
    def x(self, value: float) -> None:
        self._x = round(value, ROUND_NUMBERS)

    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, value: float) -> None:
        self._y = round(value, ROUND_NUMBERS)

    def get(self) -> tuple:
        return self.x, self.y

    def set(self, dot: tuple) -> None:
        self.x, self.y = dot

    def convert(self) -> tuple:
        """converts the dot from cordinate system where (0, 0) is the origin, to pygame's cordinate system"""
        x = WIDTH / 2 + self.x
        y = HEIGHT / 2 - self.y
        return x, y

    def copy(self):
        return Dot(self.x, self.y)

    def distance(self, dot) -> float:
        if type(dot) != Dot:
            return -1
        d = sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)
        return round(d, ROUND_NUMBERS)

    def rotate(self, origin: Self, angle: int) -> tuple:
        a = self.x - origin.x
        b = self.y - origin.y
        r = sqrt(a ** 2 + b ** 2)
        
        try:
            alpha = degrees(atan(b / a))
        except ZeroDivisionError:
            alpha = 90 if b > 0 else 270
    
        beta = radians(alpha - angle)
        x, y = floor(r * cos(beta)), floor(r * sin(beta))
        
        return x, y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'