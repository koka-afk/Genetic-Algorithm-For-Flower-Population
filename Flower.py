import random
class flower:
    def __init__(self):
        self.center_size = random.randint(1, 20)
        self.center_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.petals_number = random.randint(0, 7)
        self.petals_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.fitness = 0
    