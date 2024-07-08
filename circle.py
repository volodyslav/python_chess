from settings import *

class Circle(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((10, 10))
        
    def draw_circle(self, image_dashboard, pos):
        self.rect = self.image.get_frect(center=pos)
        image_dashboard.blit(self.image, self.rect)

    def delete_circle(self):
        self.kill()