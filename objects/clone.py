from .player import Player, Json


class Clone(Player):
    def __init__(self, json: dict) -> None:
        super().__init__(json[Json.ID])
        self.update_json(json)
    
    def update_json(self, json: dict) -> None:
        self.position = json[Json.POS]
        self.color = json[Json.COLOR]
        self.angle = json[Json.ANGLE]
        self.health = json[Json.HEALTH]