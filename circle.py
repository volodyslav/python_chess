from settings import *

class Circle(pygame.sprite.Sprite):
    def __init__(self, pos, image_dashboard) -> None:
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_frect(center=pos)
        image_dashboard.blit(self.image, self.rect)
        
    def delete_circle(self):
        self.kill()