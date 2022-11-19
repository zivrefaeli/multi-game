from pygame import draw
from pygame.surface import Surface
from .constants import BLACK, WIDTH, HEIGHT
from .dot import Dot
from .vector import Vector


class Bullet:
    SPEED = 4
    RADIUS = 1

    def __init__(self, position: Dot = Dot(), angle: int = 0) -> None:
        self.position = position
        self.angle = angle
        self.velocity = Vector(self.SPEED, self.angle)
        self.color = BLACK
    
    def update(self) -> None:
        dx, dy = self.velocity.get()
        self.position.x += dx
        self.position.y += dy

    @staticmethod
    def draw(surface: Surface, color: tuple[int, int, int], position: Dot) -> None:
        draw.circle(surface, color, position.convert(), Bullet.RADIUS)

    def display(self, surface: Surface) -> None:
        self.draw(surface, self.color, self.position)

    def in_bounds(self) -> bool:
        x, y = self.position.convert()
        return 0 <= x <= WIDTH and 0 <= y <= HEIGHT

    def __str__(self) -> str:
        return f'{self.position}, {self.angle}'