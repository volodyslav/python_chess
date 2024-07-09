from typing import Any
from settings import *
from circle import Circle

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

    def piece_color(self):
        """Return the color of the piece"""
        return self.image_name.split("_")[0]

    def move(self, dt):
        if self.selected: 
            self.distance_2top = abs(int((self.rect_dashboard_top - self.rect.center[1]) // (SQUARE_SIZE[1] * 2)))
            print(self.distance_2top)
        
    def update(self, dt) -> None:
        self.delete_path()   
                
        
    def draw_path(self, image_dashboard, right, left, top, bottom):
        """Draws path for the piece"""
        pass

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
        self.image_name = image_name
        self.pawn_color = self.piece_color()
        
        # For coordinates of the path
        self.pos_circles = []

        # Distance 
        self.distance_2top = abs(int((self.rect_dashboard_top - self.rect.center[1]) // (SQUARE_SIZE[1] * 2)))
        self.distance_2bottom = abs(int((self.rect.center[1] - self.rect_dashboard_bottom) // (SQUARE_SIZE[1] * 2)))

    def draw_path(self, image_dashboard):
        self.image_dashboard = image_dashboard
        # Find the distance from center y to top of the screen, opponent later
        
        print(self.distance_2top)
        print(self.distance_2bottom)
        # Draw circles if they are less than self.rect_dashboard_top dashboard rect
        distance = self.distance_2top if self.pawn_color == "white" else self.distance_2bottom

        if self.rect.center[1] > self.rect_dashboard_top:
            # Check first move 
            if self.first_move:
                for i in range(1, min(3, distance)):
                    if self.pawn_color == "white":
                        # Check if white color or black
                        self.pos_circles.append(Circle((self.rect.centerx - SQUARE_SIZE[0] * 3.5, self.rect.y - SQUARE_SIZE[1] * i), image_dashboard))
                    elif self.pawn_color == "black":
                        self.pos_circles.append(Circle((self.rect.centerx - SQUARE_SIZE[0] * 3.5, self.rect.y + SQUARE_SIZE[1] * i), image_dashboard))
            else:
                for i in range(1, min(2, distance)):
                    if self.pawn_color == "white":
                        self.pos_circles.append(Circle((self.rect.centerx - SQUARE_SIZE[0] * 3.5, self.rect.y - SQUARE_SIZE[1] * i), image_dashboard))
                    else:
                        self.pos_circles.append(Circle((self.rect.centerx - SQUARE_SIZE[0] * 3.5, self.rect.y + SQUARE_SIZE[1] * i), image_dashboard))
                

    def update(self, dt):
        self.pos_circles.clear()
        
    
        