from Entity import Entity


class Player(Entity):
    def __init__(self):
        super().__init__(0, 0, 48, 48 *2, "Player")
