from pygame import Surface, draw

from .constants import SOURCE_FILE, BLACK, WIDTH, HEIGHT
from .dot import Dot
from .vector import Vector


class Bullet:
    SPEED = 4
    RADIUS = 2

    def __init__(self, position: Dot = Dot(), angle: int = 0) -> None:
        self.position = position
        self.angle = angle
        self.velocity = Vector(self.SPEED, self.angle)
    
    def update(self) -> None:
        dx, dy = self.velocity.get()
        self.position.x += dx
        self.position.y += dy

    def display(self, surface: Surface) -> None:
        draw.circle(surface, BLACK, self.position.convert(), self.RADIUS)

    def in_bounds(self) -> bool:
        x, y = self.position.convert()
        return 0 <= x <= WIDTH and 0 <= y <= HEIGHT

    def __str__(self) -> str:
        return f'{self.position}, {self.angle}'


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')