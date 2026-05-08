from const import SCREEN_HEIGHT, SCREEN_WIDTH

class Player:
    def __init__(self):
        self.health = 100
        self.mhealth = 100
        self.energee = 20
        self.menergee = 20
        self.pos = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.vel = [0, 0]