from typing import Any
from settings import *

class Piece(pygame.sprite.Sprite):
    """Implements piece class"""
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(*groups)
        # Dashboard rectangles settings
        self.rect_dashboard = rect_dashboard
        self.rect_dashboard_left = self.rect_dashboard.left
        self.rect_dashboard_top = self.rect_dashboard.top
        self.rect_dashboard_right = self.rect_dashboard.right
        self.rect_dashboard_bottom = self.rect_dashboard.bottom
        

        self.image = pygame.image.load(join("img", "pieces", image_name)).convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_frect(center=pos)

        # For inceasing the size
        self.original_size = self.rect.size 
        
        self.selected = True
        

    def mouse_position(self, event, image_dashboard):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos) and self.selected:
                print(self.rect)
                self.draw_path(image_dashboard, self.rect_dashboard_right, 
                               self.rect_dashboard_left, self.rect_dashboard_top, self.rect_dashboard_bottom)
            self.selected = False
        
    def draw_path(self, image_dashboard, right, left, top, bottom):
        """Draws path for the piece"""
        pygame.draw.circle(image_dashboard, PATH_COLOR, (100, 100), 10)      



class Bishop(Piece):
    """Bishop class"""
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(image_name, rect_dashboard, pos, *groups)


class King(Piece):
    """King class"""
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(image_name, rect_dashboard, pos, *groups)


class Queen(Piece):
    """Queen class"""
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(image_name, rect_dashboard, pos, *groups)


class Rook(Piece):
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(image_name, rect_dashboard, pos, *groups)


class Knight(Piece):
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(image_name, rect_dashboard, pos, *groups)


class Pawn(Piece):
    def __init__(self, image_name, rect_dashboard, pos, *groups):
        super().__init__(image_name, rect_dashboard, pos, *groups)
        self.rect_dashboard = rect_dashboard


    def draw_path(self, image_dashboard, right, left, top, bottom):
        # Find the distance from center y to top of the screen, opponent later
        distance = abs(int((top - self.rect.center[1]) // (SQUARE_SIZE[1] * 2)))
        print(distance)
        # Draw circles if they are less than top dashboard rect
        print(self.rect.x)
        if self.rect.center[1] > top:
            for i in range(1, distance):
                pygame.draw.circle(image_dashboard, PATH_COLOR, (self.rect.x, self.rect.y + i), 10)   

    