from .constants import SOURCE_FILE, JSON_ID, JSON_COLOR, JSON_ANGLE, JSON_POS
from .player import Player


class Clone(Player):
    def __init__(self, json: dict) -> None:
        super().__init__(json[JSON_ID], True)

        self.color = json[JSON_COLOR]
        self.position = json[JSON_POS]
        self.angle = json[JSON_ANGLE]
        
        self.set_look()


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')