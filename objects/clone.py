from .constants import SOURCE_FILE, Data
from .player import Player


class Clone(Player):
    def __init__(self, json: dict) -> None:
        super().__init__(json[Data.ID])

        self.position = json[Data.POS]
        self.color = json[Data.COLOR]
        self.angle = json[Data.ANGLE]
        self.health = json[Data.HEALTH]
        

if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')