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
        
        self.selected = False
        

    def mouse_position(self, event, image_dashboard):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            self.selected = False
            if self.rect.collidepoint(mouse_pos):
                print(self.rect)
                self.selected = True
                if self.selected:
                    self.draw_path(image_dashboard, self.rect_dashboard_right, 
                               self.rect_dashboard_left, self.rect_dashboard_top, self.rect_dashboard_bottom)
                else:
                    self.delete_path()
    
                
                
        
    def draw_path(self, image_dashboard, right, left, top, bottom):
        """Draws path for the piece"""
        pygame.draw.circle(image_dashboard, PATH_COLOR, (100, 100), 10)      


    def delete_path(self):
        """Erase the path(blue circles)"""
        pass


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
        self.first_move = True

        # For coordinates of the path
        self.pos_circles = []


    def draw_path(self, image_dashboard, right, left, top, bottom):
        # Find the distance from center y to top of the screen, opponent later
        distance = abs(int((top - self.rect.center[1]) // (SQUARE_SIZE[1] * 2)))
        print(distance)
        # Draw circles if they are less than top dashboard rect
        if self.rect.center[1] > top:
            # Check first move 
            if self.first_move:
                for i in range(1, min(3, distance)):
                    self.pos_circles.append((self.rect.centerx - SQUARE_SIZE[0] * 7, self.rect.y - SQUARE_SIZE[1] * 2 * i))
            else:
                for i in range(1, min(2, distance)):
                    self.pos_circles.append((self.rect.centerx - SQUARE_SIZE[0] * 7, self.rect.y - SQUARE_SIZE[1] * 2 * i))
        # draw the path
        if self.pos_circles:
            for pos in self.pos_circles:     
                pygame.draw.circle(image_dashboard, PATH_COLOR, pos, 10)   

    def delete_path(self):
        self.pos_circles = []
        