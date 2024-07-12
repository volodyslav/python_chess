
from settings import *

class Circle(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_frect(center=pos)
       
        
    def delete_circle(self):
        self.kill()
