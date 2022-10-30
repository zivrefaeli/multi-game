import pygame
from math import atan, cos, sin, degrees, radians, sqrt
from constants import *
from random import randint as rnd

class Dot:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def copy(self):
        return Dot(self.x, self.y)

    def distance(self, dot) -> float:
        return sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)

    def __add__(self, other):
        if type(other) == Vector:        
            dx, dy = other.delta()
            self.x = round(self.x + dx, 2)
            self.y = round(self.y + dy, 2)
            return Dot(self.x, self.y)
        return Dot()

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

class Vector:
    def __init__(self, size: float = 0, angle: int = 0) -> None:
        self.size = size
        self.angle = angle
    
    def delta(self) -> tuple:
        dx = self.size * cos(radians(self.angle))
        dy = self.size * sin(radians(self.angle))
        return dx, dy

    def __add__(self, other):
        if type(other) == Vector:
            dx1, dy1 = self.delta()
            dx2, dy2 = other.delta()
            dx = dx1 + dx2
            dy = dy1 + dy2
            
            size = round(sqrt(dx ** 2 + dy ** 2), 2)
            angle = get_angle_by_delta(dx, dy)
            return Vector(size, angle)
        return Vector()

    def __str__(self) -> str:
        return f'Vector(size={self.size}, angle={self.angle}°)'

class Player:
    def __init__(self, name: str = 'Player', size: int = PLAYER_DEFAULT_SIZE, position: Dot = Dot()) -> None:
        self.position = position
        self.velocity = Vector()
        self.acceleration = Vector()

        self.name = name
        self.size = (size, size)
        self.angle = 0
        self.speed = PLAYER_DEFAULT_SPEED
        self.accelerating = False
        self.moving = False
        self.crouching = False
        self.shooting = False
        self.bullets = []

        self.skin = pygame.Surface(self.size).convert_alpha()
        self.color = random_color()
        self.skin.fill(self.color)
        body_image = pygame.image.load('./assets/player.png')
        body = pygame.transform.scale(body_image, self.size)
        self.skin.blit(body, (0, 0))

    def draw(self, screen: pygame.Surface) -> None:
        if self.shooting:
            self.shoot()

        if self.accelerating:
            self.acceleration.size = self.speed
        else:
            self.acceleration.size = -self.speed
            if self.velocity.size < 1:
                self.velocity.size = 0
                self.moving = False
        
        if self.crouching:
            self.acceleration.size *= 0.5
        
        if self.moving:
            self.velocity += self.acceleration
            self.position += self.velocity

        display_name(screen, self.name, self.position)
        display_bullets(screen, self.bullets)
        display_rotated_object(screen, self.position, self.skin, self.angle)
    
    def rotate(self, dot: tuple) -> None:
        x, y = convert_position(self.position)
        dx = dot[0] - x
        dy = y - dot[1]

        self.angle = get_angle_by_delta(dx, dy)
        
        if self.accelerating:
            self.acceleration.angle = self.angle
        else:
            self.acceleration.angle = self.velocity.angle

    def shoot(self) -> None:
        bullet = Bullet(self.position.copy(), self.angle)
        self.bullets.append(bullet)

    def hit(self, clones: list) -> None:
        for clone in clones:
            i = 0
            while i < len(self.bullets):
                bullet = self.bullets[i]
                brect = get_rotated_rect(bullet.position, bullet.skin, bullet.angle)
                rect = get_rotated_rect(clone.position, clone.skin, clone.angle)
                if pygame.Rect.colliderect(rect, brect):
                    if hitbox(bullet.position, clone.position, clone.angle, clone.size[0]):
                        del self.bullets[i]
                        continue
                i += 1

    def get_player_data(self) -> dict:
        return {
            'position': self.position.copy(),
            'name': self.name,
            'size': self.size,
            'angle': self.angle,
            'color': self.color
        }

    def __str__(self) -> str:
        return f'a={self.acceleration} | v={self.velocity} | x={self.position} | {self.moving} | {self.accelerating}'

class PlayerClone:
    def __init__(self, data: dict) -> None:
        self.position = data['position']
        self.name = data['name']
        self.size = data['size']
        self.angle = data['angle']
        self.color = data['color']

        self.skin = pygame.Surface(self.size).convert_alpha()
        self.skin.fill(self.color)
        body_image = pygame.image.load('./assets/player.png')
        body = pygame.transform.scale(body_image, self.size)
        self.skin.blit(body, (0, 0))

    def update(self, data: dict) -> None:
        self.position = data['position']
        self.angle = data['angle']

    def draw(self, screen: pygame.Surface) -> None:
        display_name(screen, self.name, self.position)
        display_rotated_object(screen, self.position, self.skin, self.angle)

class Bullet:
    def __init__(self, position: Dot = Dot(), angle: int = 0) -> None:
        self.position = position
        self.angle = angle
        self.velocity = Vector(size=BULLET_DEFAULT_SPEED, angle=self.angle)
    
        self.skin = pygame.image.load('./assets/bullet.png')

    def draw(self, screen: pygame.Surface) -> None:
        self.position += self.velocity
        display_rotated_object(screen, self.position, self.skin, self.angle)

    def in_bounds(self) -> bool:
        x, y = convert_position(self.position)
        return 0 <= x <= WIDTH and 0 <= y <= HEIGHT

    def __str__(self) -> str:
        return f'{self.velocity} | {self.position}'

def convert_position(position: Dot) -> tuple:
    """position: a point in a cordinate system where (0, 0) is the origin"""
    new_x = WIDTH / 2 + position.x
    new_y = HEIGHT / 2 - position.y
    return new_x, new_y

def random_color() -> tuple:
    return (rnd(0, 255), rnd(0, 255), rnd(0, 255))

def get_angle_by_delta(dx: float, dy: float) -> int:
    if dy == 0:
        if dx >= 0:
            return 0
        return 180
    
    if dx == 0:
        if dy > 0:
            return 90
        return 270
    
    alpha = int(degrees(atan(dy / dx)))
    if dx > 0:
        if dy > 0:
            return alpha
        return 360 + alpha
    return 180 + alpha

def get_rotated_rect(position: Dot, skin: pygame.Surface, angle: int) -> pygame.Surface:
    return pygame.transform.rotate(skin, angle).get_rect(center=convert_position(position))

def display_rotated_object(screen: pygame.Surface, position: Dot, skin: pygame.Surface, angle: int) -> None:
    rotated = pygame.transform.rotate(skin, angle)
    rect = rotated.get_rect(center=convert_position(position))
    screen.blit(rotated, rect)

def display_bullets(screen: pygame.Surface, bullets: list) -> None:
    i = 0
    while i < len(bullets):
        bullet = bullets[i]
        bullet.draw(screen)

        if not bullet.in_bounds():
            del bullets[i]
        else:
            i += 1

def display_name(screen: pygame.Surface, name: str, position: Dot) -> None:
    text = PLAYER_NAME_FONT.render(name, True, BLACK)
    x, y = convert_position(position)
    rect = text.get_rect(center=(x, y - PLAYER_NAME_DELTA))
    screen.blit(text, rect)

def hitbox(bullet_dot: Dot, clone_dot: Dot, clone_angle: int, clone_size: int) -> bool:
    # relative dot (a, b) to clone_dot as origin (0, 0)
    a = bullet_dot.x - clone_dot.x
    b = bullet_dot.y - clone_dot.y
    R = sqrt(a ** 2 + b ** 2)

    alpha = 0 if 0 in [a, b] else degrees(atan(b / a)) 
    arg = (alpha - clone_angle + 360) % 360 # arg > 0

    new_dot = Dot(round(R * cos(radians(arg))), round(R * sin(radians(arg))))
    d = clone_size / 2

    return -d <= new_dot.x <= d and -d <= new_dot.y <= d

if __name__ == '__main__':
    file_name = __file__.split('\\')[-1]
    print(f'{file_name} is a source file')