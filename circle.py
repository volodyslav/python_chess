
from settings import *

class Circle(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((CIRCLE_SIZE, CIRCLE_SIZE))
        self.rect = self.image.get_frect(center=pos)
       
class CircleEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((CIRCLE_SIZE, CIRCLE_SIZE))
        self.rect = self.image.get_frect(center=pos)
        self.image.fill("red")

class CircleCheck(pygame.sprite.Sprite):
    def __init__(self, color,  pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((CIRCLE_SIZE, CIRCLE_SIZE))
        self.rect = self.image.get_frect(center=pos)
        self.image.fill(color)