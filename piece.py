
from settings import *
from circle import Circle

class Piece(pygame.sprite.Sprite):
    """Class for all pieces"""
    def __init__(self, image_path, pos, color, piece_name, *groups):
        super().__init__(*groups)
        self.color = color
        self.piece_name = piece_name
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.2, self.image.get_height() * 1.2))
        self.rect = self.image.get_frect(center=pos)

        self.speed = 10

    def move(self, square_position_x, square_position_y, piece_name):
        if piece_name.split(".")[0] == "pawn":
            self.rect.centerx = (square_position_x + 0.5) * SQUARE_SIZE 
            self.rect.centery = (square_position_y + 0.5) * SQUARE_SIZE 
        
    
    
   