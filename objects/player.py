from pygame import Surface, font, transform, image

from .constants import SOURCE_FILE, PLAYER_SIZE, BLACK, ID_DELTA, PLAYER_DEFAULT_SPEED, JSON_ID, JSON_COLOR, JSON_ANGLE, JSON_POS
from .dot import Dot
from .methods import Methods
from .vector import Vector

class Player:
    def __init__(self, id: str = 'Player', clone: bool = False) -> None:
        self.id = id

        self.position = Dot()
        self.velocity = Vector()
        self.acceleration = Vector()
        
        self.angle = 0
        self.size = (PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_DEFAULT_SPEED
        self.accelerating = False
        self.moving = False
        self.crouching = False

        self.color = Methods.random_color()
        self.body = Surface(self.size).convert_alpha()

        if not clone:
            self.set_look()
    
    def set_look(self) -> None:
        self.body.fill(self.color)

        skin = image.load('./assets/player.png')
        scaled_skin = transform.scale(skin, self.size)
        self.body.blit(scaled_skin, (0, 0))

    def rotate_to(self, dot: tuple) -> None:
        x, y = self.position.convert()
        dx = dot[0] - x
        dy = y - dot[1]

        self.angle = (Methods.get_angle_by_delta(dx, dy) + 360) % 360
        
        if self.accelerating:
            self.acceleration.angle = self.angle
        else:
            self.acceleration.angle = self.velocity.angle

    def update(self) -> None:
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

            dx, dy = self.velocity.get()
            self.position.x += dx
            self.position.y += dy

    def display(self, surface: Surface) -> None:
        self.update()

        # player surface
        rotated_body = transform.rotate(self.body, self.angle)
        body_rect = rotated_body.get_rect(center=self.position.convert())

        # player id surface
        id_font = font.SysFont('Times', 16)
        text = id_font.render(self.id, True, BLACK)
        text_dot = self.position.copy()
        text_dot.y += ID_DELTA
        text_rect = text.get_rect(center=text_dot.convert())

        surface.blit(rotated_body, body_rect)
        surface.blit(text, text_rect)

    def json(self) -> dict:
        return {
            JSON_ID: self.id,
            JSON_POS: self.position,
            JSON_COLOR: self.color,
            JSON_ANGLE: self.angle
        }


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')