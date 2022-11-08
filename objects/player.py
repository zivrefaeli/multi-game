from pygame import Surface, font, transform, image
from time import sleep
from threading import Thread

from .constants import SOURCE_FILE, BLACK, JSON_ID, JSON_COLOR, JSON_ANGLE, JSON_POS
from .dot import Dot
from .methods import Methods
from .vector import Vector
from .bullet import Bullet

class Player:
    SIZE = 50 # px
    DIMENTIONS = (SIZE, SIZE)
    ID_DELTA = int(SIZE / 2 + 15)
    SPEED = .5 # px/frame
    MAX_AMMO = 30
    RELOAD_TIME = 1 # sec

    def __init__(self, id: str = 'Player', clone: bool = False) -> None:
        self.id = id

        self.position = Dot()
        self.velocity = Vector()
        self.acceleration = Vector()
        
        self.angle = 0
        self.moving = False
        self.accelerating = False
        self.crouching = False

        self.bullets = []
        self.shooting = False
        self.reloading = False
        self.ammo = self.MAX_AMMO

        self.color = Methods.random_color()
        self.body = Surface(self.DIMENTIONS).convert_alpha()

        if not clone:
            self.set_look()

    @property
    def angle(self) -> int:
        return self._angle

    @angle.setter
    def angle(self, value: int) -> None:
        self._angle = (value + 360) % 360
    
    def set_look(self) -> None:
        self.body.fill(self.color)

        skin = image.load('./assets/player.png')
        scaled_skin = transform.scale(skin, self.DIMENTIONS)
        self.body.blit(scaled_skin, (0, 0))

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

        rotated_body = transform.rotate(self.body, self.angle)
        body_rect = rotated_body.get_rect(center=self.position.convert())

        self.display_bullets(surface)
        self.display_id(surface)
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
            bullet = Bullet(self.position.copy(), self.angle)
            self.bullets.append(bullet)
            self.ammo -= 1
        elif not self.reloading:
            self.reloading = True
            reload_thread = Thread(target=self.reload)
            reload_thread.start()

    def reload(self) -> None:
        print('reloading')
        sleep(self.RELOAD_TIME)
        self.reloading = False
        self.ammo = self.MAX_AMMO

    def json(self) -> dict:
        return {
            JSON_ID: self.id,
            JSON_POS: self.position,
            JSON_COLOR: self.color,
            JSON_ANGLE: self.angle
        }

    def __str__(self) -> str:
        return f'[{self.id}]: {{{self.position}, {self.angle}}}'


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')