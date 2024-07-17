
from settings import *


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
        # First move for pawns
        self.first_move = False



    def move_black_pawn(self, square_position_x, square_position_y):
        """Move the black pawns"""
        self.rect.centerx = (square_position_x + 0.5) * SQUARE_SIZE 
        self.rect.centery = (square_position_y + 0.5) * SQUARE_SIZE 
        
    def move_black_rook(self, square_position_x, square_position_y, rect_pos_x, rect_pos_y):
        """Move the black rooks"""
        if square_position_x == rect_pos_x: # Check movement horizontally 
            self.rect.centerx = (square_position_x + 0.5) * SQUARE_SIZE 
            self.rect.centery = (square_position_y + 0.5) * SQUARE_SIZE 
        elif square_position_y == rect_pos_y: # Check movement vertically
            self.rect.centerx = (square_position_x + 0.5) * SQUARE_SIZE 
            self.rect.centery = (square_position_y + 0.5) * SQUARE_SIZE 
    

    def move_knight(self, square_position_x, square_position_y, rect_pos_x, rect_pos_y):
        self.rect.centerx = (square_position_x + 0.5) * SQUARE_SIZE 
        self.rect.centery = (square_position_y + 0.5) * SQUARE_SIZE 
    
    def move_bishop(self, square_position_x, square_position_y, rect_pos_x, rect_pos_y):
        self.rect.centerx = (square_position_x + 0.5) * SQUARE_SIZE 
        self.rect.centery = (square_position_y + 0.5) * SQUARE_SIZE 
    