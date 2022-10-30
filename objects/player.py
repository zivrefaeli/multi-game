from pygame import Surface, font

from .constants import SOURCE_FILE, PLAYER_SIZE, BLACK, ID_DELTA
from .dot import Dot
from .methods import Methods

class Player:
    def __init__(self, id: str = 'Player') -> None:
        self.id = id
        self.position = Dot()
        self.body = Surface((PLAYER_SIZE, PLAYER_SIZE))

        # player look
        self.body.fill(Methods.random_color())

    def display(self, surface: Surface) -> None:
        rect = self.body.get_rect(center=self.position.convert())

        id_font = font.SysFont('Times', 16)
        text = id_font.render(self.id, True, BLACK)
        text_dot = self.position.copy()
        text_dot.y += ID_DELTA
        text_rect = text.get_rect(center=text_dot.convert())

        surface.blit(self.body, rect)
        surface.blit(text, text_rect)


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')