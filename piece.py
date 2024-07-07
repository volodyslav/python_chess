from settings import *

class Piece(pygame.sprite.Sprite):
    """Implements piece class"""
    def __init__(self, image_name, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join("img", "pieces", image_name)).convert_alpha()
        self.rect = self.image.get_frect(center=pos)