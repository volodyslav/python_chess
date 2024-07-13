from settings import *
from piece import Piece
from circle import Circle



class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = [[None for _ in range(8)] for _ in range(8)] 

        self.black_images = [["rook.png", "knight.png", "bishop.png", "queen.png", "king.png", "bishop.png", "knight.png", "rook.png"], ["pawn.png" for _ in range(8)]]
        self.white_images = [["pawn.png" for _ in range(8)], ["rook.png", "knight.png", "bishop.png", "queen.png", "king.png", "bishop.png", "knight.png", "rook.png"]]

        # Dashboard
        self.image_dashboard = pygame.image.load(join("img", "board.png")).convert_alpha()
        self.rect_dashboard = self.image_dashboard.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.dash_left, self.dash_top = self.rect_dashboard.left, self.rect_dashboard.top
        # All group
        self.group_sprites = pygame.sprite.Group()

        # Black  and white groups
        self.black_group = pygame.sprite.Group()
        self.white_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        
        # fOR MOVING
        self.selected_piece = None
        self.move_is_over = False

        self.can_move = False # Check if nothing between piece and square to move 

        # Circles for movement
        self.circles = [] 
        
        self.draw_board_pieces()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.move_is_over = False # Check if movement is over, let's go to the next piece
                    mouse_pos = event.pos
                    print(mouse_pos)
                    self.check_movement(mouse_pos)
                    self.select_piece(mouse_pos)
       
            self.show_screen()
           
    def select_piece(self, mouse_pos):
        """Selects a piece"""
        self.selected_piece = None
        
        for piece in self.black_group:
            if piece.rect.collidepoint(mouse_pos):
                if not self.selected_piece and not self.move_is_over:
                    self.selected_piece = piece # select a piece which is just selected
                    self.piece_name = self.selected_piece.piece_name.split(".")[0] # Just a name like pawn etc
                    self.piece_color = self.selected_piece.color

                    self.move_diraction = 1 if self.piece_color == "black" else -1 # Check the piece's color

                     # Draw the circles
                   # Draw circles
                    
                    if self.piece_name == "pawn":
                        self.number_move_pawn = 2 if self.selected_piece.first_move else 3
                        for i in range(1, self.number_move_pawn):
                            self.circles.append(Circle(((self.selected_piece.rect.centerx + 0.5), (self.selected_piece.rect.centery + 0.5) + SQUARE_SIZE * i), self.group_sprites))
                       
                    elif self.piece_name == "rook":
                        for i in range(8):
                            self.circles.append(Circle(((self.selected_piece.rect.centerx + 0.5), (self.selected_piece.rect.centery + 0.5) + SQUARE_SIZE * i), self.group_sprites))
                            self.circles.append(Circle(((self.selected_piece.rect.centerx + 0.5) + SQUARE_SIZE * i, (self.selected_piece.rect.centery + 0.5) ), self.group_sprites))
                    
                    #self.move_is_over = False 
                    print(self.selected_piece.piece_name)   
            

    def check_movement(self, mouse_pos):
        """Check if the piece can move"""
        if self.selected_piece and not self.move_is_over:
            square_position_y = mouse_pos[1] // SQUARE_SIZE # Shows the rows
            square_position_x = mouse_pos[0] // SQUARE_SIZE # Shows the columns
            print("Square pos ", square_position_y, square_position_x)

            rect_pos_y = int(self.selected_piece.rect.y // SQUARE_SIZE) # Rect pos y
            rect_pos_x = int(self.selected_piece.rect.x // SQUARE_SIZE) # Rect pos x
            print("Rect pos ", rect_pos_y, rect_pos_x)
            
            # Checks if we can move when there is None in the next square 
            
            self.can_move_rook = True
            # Check rook to move
            for k in range(rect_pos_y + 1, square_position_y + 1):
                if self.board[k][rect_pos_x] != None:
                    self.selected_piece.move_rook_vertical = True
                    self.can_move_rook = False 
            for k in range(rect_pos_x + 1, square_position_x + 1):
                if self.board[rect_pos_y][k] != None:
                    self.selected_piece.move_rook_horizontal = True
                    self.can_move_rook = False 
            for k in range(square_position_y, rect_pos_y + 1):
                if self.board[k][rect_pos_x] != None:
                    self.selected_piece.move_rook_vertical = True
            for k in range(square_position_x, rect_pos_x + 1, ):
                if self.board[rect_pos_y][k] != None:
                    self.selected_piece.move_rook_horizontal = True
                    self.can_move_rook = False 



            self.can_move_pawn = True
            # Check pawn to move
            for k in range(rect_pos_y + 1, square_position_y + 1):
                if self.board[k][rect_pos_x] != None:
                    self.can_move_pawn = False
                    
                

            move_squares = 2 if self.selected_piece.first_move else 3 # Checks first move 
            if 0 <= square_position_x <= 7 and 0 <= square_position_y <= 7: # Check if it mouse pos 0 <= pos <= 7 
                if self.piece_name == "pawn" and square_position_x == rect_pos_x and square_position_y < rect_pos_y + move_squares and not rect_pos_y > square_position_y: # Check x == x cant move if x + 1 ;and 3 = 2 squares to move; cant move back:  # Check only a black pawn
    
                    if self.can_move_pawn:
                        self.selected_piece.move_black_pawn(square_position_x, square_position_y)
                        print("Move!")
                        self.selected_piece.first_move = True # Checks first move
                        print(self.selected_piece.piece_name)
                        # Change postions in board list
                        self.change_board_position(square_position_y, square_position_x, rect_pos_y, rect_pos_x)

                        self.selected_piece = None # None selected
                        self.move_is_over = True # Cant move anymore the selected piece
                elif self.piece_name == "rook" and self.can_move_rook:  # Check only a black rook
                    self.selected_piece.move_black_rook(square_position_x, square_position_y, rect_pos_x, rect_pos_y)
                    print("Move!")
                    self.selected_piece.first_move = True # Checks first move
                    print(self.selected_piece.piece_name)
                    self.change_board_position(square_position_y, square_position_x, rect_pos_y, rect_pos_x)
                    self.selected_piece = None # None selected
                    self.move_is_over = True # Cant move anymore the selected piece
                
            print(self.board)
            # Delete all circles
            self.delete_circles()

    def delete_circles(self):
        """Delete all circles after a movement"""    
        for circle in self.circles:
            circle.kill()      

    def change_board_position(self, square_position_y, square_position_x, rect_pos_y, rect_pos_x):
        """Changes the piece's board positions"""
        self.board[square_position_y][square_position_x] = self.board[rect_pos_y][rect_pos_x]
        self.board[rect_pos_y][rect_pos_x] = None


    def draw_board_pieces(self):
        """Draw the pieces on the screen"""
        for j in range(2):
            for i in range(8):
                self.board[j][i] = Piece(join("img", "black", self.black_images[j][i]), 
                                         (self.dash_left + SQUARE_SIZE * (i + 0.5), self.dash_top + SQUARE_SIZE * (j + 0.5)), 
                                          "black", self.black_images[j][i], 
                                         (self.group_sprites, self.black_group))

        for j in range(2):
            for i in range(8):
                self.board[j+6][i] = Piece(join("img", "white", self.white_images[j][i]), 
                                         (self.dash_left + SQUARE_SIZE * (i + 0.5), self.dash_top + SQUARE_SIZE * (j + 6.5)), 
                                         "white", self.white_images[j][i], 
                                         (self.group_sprites, self.white_group))
        


    def show_screen(self):
        dt = self.clock.tick() / 1000
        self.screen.fill("gray")

        # Draw the dashboard
        self.screen.blit(self.image_dashboard, self.rect_dashboard)

        # Draw all sprites
        self.group_sprites.draw(self.screen)
        self.group_sprites.update(dt)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
