from pygame import Surface, image, transform

from .constants import RED, SOURCE_FILE
from .dot import Dot


class HealthBar:
    DIMENTIONS = (50, 10)
    PADDING = 1
    FULL_HEALH = 100

    def __init__(self) -> None:
        self.health = self.FULL_HEALH

    def display(self, surface: Surface, dot: Dot) -> None:
        skin = image.load('./assets/healh_bar.png')
        body = transform.scale(skin, self.DIMENTIONS)
    
        width, height = self.DIMENTIONS
        width -= self.PADDING * 2
        height -= self.PADDING * 2
        bar = Surface((int(width * self.health / 100), int(height)))
        bar_rect = bar.fill(RED)
        bar_rect.topleft = (self.PADDING, self.PADDING)
        body.blit(bar, bar_rect)

        rect = body.get_rect(center=dot.convert())
        surface.blit(body, rect)


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')