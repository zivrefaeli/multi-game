from time import sleep
from math import sqrt
from threading import Thread
from pygame import font, transform, image
from pygame.surface import Surface
from .constants import BLACK, TRANSPARENT
from .dot import Dot
from .methods import Methods
from .vector import Vector
from .bullet import Bullet


class Json:
    ID = 'id'
    POS = 'position'
    COLOR = 'color'
    ANGLE = 'angle'
    HEALTH = 'health'
    BULLETS = 'bullets'


class Player:
    SIZE = 50 # px
    DIMENTIONS = (SIZE, SIZE)
    ID_DELTA = int(SIZE / 2 + 15)
    RADIUS = sqrt(2) / 2 * SIZE
    SPEED = .5 # px/frame
    MAX_AMMO = 30
    RELOAD_TIME = 1 # sec
    FULL_HEALTH = 100

    def __init__(self, id: str = 'Player') -> None:
        self.id = id

        self.position = Dot()
        self.velocity = Vector()
        self.acceleration = Vector()
        
        self.angle = 0
        self.moving = False
        self.accelerating = False
        self.crouching = False

        self.bullets: list[Bullet] = []
        self.shooting = False
        self.ammo = self.MAX_AMMO

        self.color = Methods.random_color()
        self.health = self.FULL_HEALTH

        self.set_icon()

    @property
    def angle(self) -> int:
        return self._angle

    @angle.setter
    def angle(self, value: int) -> None:
        self._angle = (value + 360) % 360

    def set_icon(self) -> None:
        skin = image.load('./assets/player.png')
        self.scaled_skin = transform.scale(skin, self.DIMENTIONS)

        self.icon = Surface(self.DIMENTIONS)
        self.icon.fill(self.color)
        self.icon.blit(self.scaled_skin, (0, 0))

    def rotate_to(self, dot: tuple) -> None:
        x, y = self.position.convert()
        dx = dot[0] - x
        dy = y - dot[1]

        self.angle = Methods.get_angle_by_delta(dx, dy)
        
        if self.accelerating:
            self.acceleration.angle = self.angle
        else:
            self.acceleration.angle = self.velocity.angle

    def update(self) -> None:
        if self.accelerating:
            self.acceleration.size = self.SPEED
        else:
            self.acceleration.size = -self.SPEED
            if self.velocity.size < 1:
                self.velocity.size = 0
                self.moving = False
        
        if self.crouching:
            self.acceleration.size *= 0.5
        
        if self.moving:
            self.velocity += self.acceleration

            dx, dy = self.velocity.get()
            self.position.x += dx
            self.position.y += dy

    def display(self, surface: Surface) -> None:
        self.update()

        self.display_bullets(surface)
        self.display_id(surface)
        self.display_body(surface)

    def display_body(self, surface: Surface) -> None:
        body = Surface(self.DIMENTIONS).convert_alpha()
        body.fill(TRANSPARENT)

        body_fill = Surface((int(self.DIMENTIONS[0] * self.health / 100), self.DIMENTIONS[1]))
        body.blit(body_fill, body_fill.fill(self.color))
        body.blit(self.scaled_skin, (0, 0))

        rotated_body = transform.rotate(body, self.angle)
        body_rect = rotated_body.get_rect(center=self.position.convert())
        surface.blit(rotated_body, body_rect)

    def display_id(self, surface: Surface) -> None:
        id_font = font.SysFont('Times', 16)
        
        text = id_font.render(self.id, True, BLACK)
        text_dot = self.position.copy()
        text_dot.y += self.ID_DELTA
        
        text_rect = text.get_rect(center=text_dot.convert())
        surface.blit(text, text_rect)

    def display_bullets(self, surface: Surface) -> None:
        index = 0
        while index < len(self.bullets):
            bullet = self.bullets[index]

            bullet.update()
            if bullet.in_bounds():
                bullet.display(surface)
            else:
                self.bullets.pop(index)
            
            index += 1

    def shoot(self) -> None:
        if self.ammo > 0:
            bullet = Bullet(self.position.copy(), self.angle, self.color)
            self.bullets.append(bullet)
            self.ammo -= 1
            if self.ammo == 0:
                reload_thread = Thread(target=self.reload)
                reload_thread.setName('Reload')
                reload_thread.start()

    def reload(self) -> None:
        sleep(self.RELOAD_TIME)
        self.ammo = self.MAX_AMMO

    def hit(self, other_pos: Dot, other_angle: int) -> int:
        damage = 0
        i = 0
        d = self.SIZE / 2

        while i < len(self.bullets):
            bullet = self.bullets[i]
            if bullet.position.distance(other_pos) > self.RADIUS:
                i += 1
                continue
            
            x, y = bullet.position.rotate(other_pos, other_angle)
            if -d <= x <= d and -d <= y <= d:
                damage += 1
                self.bullets.pop(i)
            else:
                i += 1
        return damage

    def json(self) -> dict:
        return {
            Json.ID: self.id,
            Json.POS: self.position,
            Json.COLOR: self.color,
            Json.ANGLE: self.angle,
            Json.HEALTH: self.health,
            Json.BULLETS: [bullet.position for bullet in self.bullets]
        }

    def __str__(self) -> str:
        return f'[{self.id}]: {{{self.position}, {self.angle}}}'