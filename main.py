from settings import *
from piece import Piece
from circle import *



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
        self.piece_group = pygame.sprite.Group()
        self.black_group = pygame.sprite.Group()
        self.white_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        
        # For checking if king check 
        self.check_white_king = False
        self.check_black_king = False
        #self.check_pos_x, self.check_pos_y = 0, 0 # Pos of the piece which makes the check
        self.position_king_checked = [] # When king is checked position where other peaces can move to protect the king
       
        self.circles_ckeck = [] # For circles to draw
        self.circle_king_cant_move = []
        self.circle_white_king_cant_move = []

        # For checking if king can be checked if a piece which protects the king moves
        self.cant_move_king_can_be_checked_black_x = [] # black
        self.cant_move_king_can_be_checked_black_y = [] # black
        self.cant_move_king_can_be_checked_white_x = [] # white
        self.cant_move_king_can_be_checked_white_y = [] # white

        self.cant_move_king_can_be_checked_black_x_bishop = [] # black
        self.cant_move_king_can_be_checked_black_y_bishop = [] # black
        self.cant_move_king_can_be_checked_white_x_bishop = [] # white
        self.cant_move_king_can_be_checked_white_y_bishop = [] # white

        self.cant_move_king_can_be_checked_circles = []

        # fOR MOVING
        self.selected_piece = None
        self.move_is_over = False

        self.can_move = False # Check if nothing between piece and square to move 

        self.piece_color_move = True # Check color before moving
        # Circles for movement
        self.circles = [] 
        # Circles for beating
        self.circle_enemy = []

        self.enemy_color = "black" # Checks enemy's color
        
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
            self.check_king_check() # check ckeck or ckeckmate

    def select_piece(self, mouse_pos):
        """Selects a piece"""
        self.selected_piece = None
    
        for piece in self.piece_group:
            if piece.rect.collidepoint(mouse_pos):
                if not self.selected_piece and not self.move_is_over:
                    self.selected_piece = piece # select a piece which is just selected
                    self.piece_name = self.selected_piece.piece_name.split(".")[0] # Just a name like pawn etc
                    self.piece_color = self.selected_piece.color
                    print(self.selected_piece.piece_name)   
                    # Rect position on the board
                    self.rect_pos_y = int(self.selected_piece.rect.y // SQUARE_SIZE) # Rect pos y
                    self.rect_pos_x = int(self.selected_piece.rect.x // SQUARE_SIZE) # Rect pos x
                    print("Rect pos ", self.rect_pos_y, self.rect_pos_x)
                    print(f"King checked white = {self.check_white_king}, black = {self.check_black_king}")
                    print(self.board)
                    # Check when king ckecked and the piece with the same color cant move
                    self.cant_move_black_pieces = True if (self.board[self.rect_pos_y][self.rect_pos_x] is not None and self.board[self.rect_pos_y][self.rect_pos_x].color == "black" and self.check_black_king) else False
                    self.cant_move_white_pieces = True if (self.board[self.rect_pos_y][self.rect_pos_x] is not None and self.board[self.rect_pos_y][self.rect_pos_x].color == "white" and self.check_white_king) else False

                    self.move_direction = 1 if self.piece_color == "black" else -1 # Check the piece's color

                    if self.piece_color == "white" and self.piece_color_move: # only white can move
                        self.check_piece_name()
                    elif self.piece_color == "black" and not self.piece_color_move: # only black can move
                        self.check_piece_name()
                         
    def check_piece_name(self):
        """Draw the circles"""
        if self.piece_name == "pawn":
            self.draw_pawn_circle()
        elif self.piece_name == "rook":
            self.draw_rook_circle()
        elif self.piece_name == "knight":
            self.draw_knight_circle()
        elif self.piece_name == "bishop":
            self.draw_bishop_circle()
        elif self.piece_name == 'queen':
            self.draw_queen_circle()
        elif self.piece_name == 'king':
            self.draw_king_circle()

    def king_is_not_checked(self):
        """Set false to check of the king"""
        self.check_black_king = False # set to false if move king from enemy or add protection
        self.check_white_king = False    

        # When you move your piece and not checkmate clear the list 
        self.position_king_checked.clear()

    def draw_king_knight_circles_x(self, i, knight_y_pos, color):
        """Draws circles on y"""
        if  0 <= i < 8: # Check forward y +
            if 0 <= knight_y_pos + 2 < 8: 
                new_target = self.board[knight_y_pos + 2][i]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos + 2 + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((i, knight_y_pos + 2)) # Cant move here
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos + 2 + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((i, knight_y_pos + 2)) # Cant move here

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check knight {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos + 2 + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((i, knight_y_pos + 2)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((i, knight_y_pos + 2)) # Cant move here
            
            if  0 <= knight_y_pos - 2 < 8:
                new_target = self.board[knight_y_pos - 2][i]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black":
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos - 2 + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((i, knight_y_pos - 2)) # Cant move here
                    elif new_target.color == "white" and color == "white":
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos - 2 + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((i, knight_y_pos - 2)) # Cant move here

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check knight {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos - 2 + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((i, knight_y_pos - 2)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((i, knight_y_pos - 2)) # Cant move here

    def draw_king_knight_circles_y(self, i, knight_y_pos, color):
        """Draws circles on y"""
        if 0 <= i < 8: # check right x +
            if 0 <= knight_y_pos + 1 < 8: 
                new_target = self.board[knight_y_pos + 1][i]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black":
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos + 1 + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((i, knight_y_pos + 1)) # Cant move here
                    if new_target.color == "white" and color == "white":
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos + 1 + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((i, knight_y_pos + 1)) # Cant move here

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check knight {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos + 1 + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((i, knight_y_pos + 1)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((i, knight_y_pos + 1)) # Cant move here

                

            if 0 <= knight_y_pos - 1 < 8: 
                new_target = self.board[knight_y_pos - 1][i]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black":
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos - 1 + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((i, knight_y_pos - 1)) # Cant move here
                    if new_target.color == "white" and color == "white":
                        #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos - 1 + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((i, knight_y_pos - 1)) # Cant move here
                  
            
                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check knight {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("red", 14, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (knight_y_pos - 1 + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((i, knight_y_pos - 1)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((i, knight_y_pos - 1)) # Cant move here

    def check_king_knight_circle(self, j, i, color):  
        # Check from y rect to x + 1
        knight_x_pos, knight_y_pos = i, j

        for i in range(knight_x_pos + 1, knight_x_pos + 2):
            self.draw_king_knight_circles_x(i, knight_y_pos, color)

        for i in range(knight_x_pos + 2, knight_x_pos + 3):
            self.draw_king_knight_circles_y(i, knight_y_pos, color)

        # Check from y rect to x - 1
        for i in range(knight_x_pos - 1, knight_x_pos - 2,  -1): 
            self.draw_king_knight_circles_x(i, knight_y_pos, color)

        for i in range(knight_x_pos - 2, knight_x_pos - 3, -1):
            self.draw_king_knight_circles_y(i, knight_y_pos, color)

    def check_king_bishop_circles(self, j, i, color):
        # Circle for movement
        bishop_x, bishop_y = i, j

        # Check down with postive x
        bishop_right_x = bishop_x
        for i in range(bishop_y + 1, 8):
            bishop_right_x += 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                new_target = self.board[i][bishop_right_x]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 14, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 14, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    else: # Cant check over a piece
                        break
            

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check bishop {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True
 
                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("orange", 14, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here

            
                else:
                    break # Check enemy color

        # Check up with negative x
        bishop_right_x = bishop_x
        for i in range(bishop_y - 1, -1, -1):
            bishop_right_x -= 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                new_target = self.board[i][bishop_right_x]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black": # If new target is None # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    else: # Cant check over a piece
                        break
            

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check bishop {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
            
                else:
                    break # Check enemy color

        # Check down with native x
        bishop_right_x = bishop_x
        for i in range(bishop_y + 1, 8):
            bishop_right_x -= 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                new_target = self.board[i][bishop_right_x]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    else: # Cant check over a piece
                        break
            

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check bishop {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        
            
                else:
                    break # Check enemy color

        # Check up with positive x
        bishop_right_x = bishop_x
        for i in range(bishop_y - 1, -1, -1):
            bishop_right_x += 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                new_target = self.board[i][bishop_right_x]
                if new_target is not None and new_target.piece_name != "king.png":  
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
                        break
                    else: # Cant check over a piece
                        break

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check bishop {new_target.color} king")
                    #Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("orange", 10, (SQUARE_SIZE * (bishop_right_x + 0.5), SQUARE_SIZE * (i + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((bishop_right_x, i)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((bishop_right_x, i)) # Cant move here
                else:
                    break # Check enemy color

    def check_king_rook_circles(self, j, i, color):
        """Append x and y to list check circles for rook"""
        for ey in range(j + 1, 8): # From top to bottom
            if 0 <= ey < 8 and 0 <= i < 8 :
                new_target = self.board[ey][i] # Pos where to draw a circle
                if new_target is not None and new_target.piece_name != "king.png": 
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((i, ey)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((i, ey)) # Cant move here
                        break
                    else: # Cant do
                        break

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check rook {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((i, ey)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((i, ey)) # Cant move here

            
                else:
                    break # Check enemy color

        for ey in range(j - 1, -1, -1): # From bottom to top
            if 0 <= ey < 8 and 0 <= i < 8 :
                new_target = self.board[ey][i]
                if new_target is not None and new_target.piece_name != "king.png":
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((i, ey)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((i, ey)) # Cant move here
                        break
                    else: # Cant do
                        break
                

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check rook {new_target.color} king")
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is enemy
                    #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((i, ey)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((i, ey))
                    
            
                else:
                    break

        for ex in range(i + 1, 8): # From left to right
            if 0 <= ex < 8 and 0 <= j < 8 :
                new_target = self.board[j][ex]
                if new_target is not None and new_target.piece_name != "king.png":
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (j + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((ex, j)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (j + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((ex, j)) # Cant move here
                        break
                    else: # Cant do
                        break
                

                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check rook {new_target.color} king")
                   # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True
                
                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (j + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((ex, j)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((ex, j)) # Cant move here

            
                else:
                    break # Check enemy color   

        for ex in range(i - 1, -1, -1): # From right to left
            if 0 <= ex < 8 and 0 <= j < 8 :
                new_target = self.board[j][ex]
                if new_target is not None and new_target.piece_name != "king.png":
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (j + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((ex, j)) # Cant move here
                        break
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (j + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((ex, j)) # Cant move here
                        break
                    else: # Cant do
                        break
                
                elif new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    #print(f"Check rook {new_target.color} king")    
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("blue", 10, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (j + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((ex, j)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((ex, j)) # Cant move here
                else:
                    break # Check enemy color 

    def check_king_pawn_circle(self, j, i, color):     
        # enemy circle
        mowe_direction = 1 if color == "black" else -1 # Direction of the pawns
        for ex in range(i - 1, i + 2, 2): # Kill from x-1 and x + 2
            new_y = j + 1 * mowe_direction
            if 0 <= ex < 8 and 0 <= new_y < 8:
                new_target = self.board[new_y][ex]
                if new_target is not None and new_target.piece_name == "king.png" and new_target.color != color:
                    # Check based on the color 
                    if new_target.color == "black":
                        self.check_black_king = True
                    elif new_target.color == "white":
                        self.check_white_king = True
                if new_target is not None:
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("yellow", 18, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (new_y + 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((ex, new_y)) # Cant move here
                    if new_target.color == "white" and color == "white": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("yellow", 18, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (new_y + 0.5)), self.group_sprites)) 
                        self.circle_white_king_cant_move.append((ex, new_y)) # Cant move here

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("yellow", 18, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (new_y + 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((ex, new_y)) # Cant move here
                    if color == "white":
                        self.circle_white_king_cant_move.append((ex, new_y))
                else:
                    break # Check enemy color

    def check_king_king_circle(self, j, i, color):
        king_pos_x, king_pos_y = i, j
        # Side right and left
        if 0 <= king_pos_x + 1 < 8 and 0 <= king_pos_y < 8: # No circles if they are blue
            new_target = self.board[king_pos_y][king_pos_x + 1]
            if new_target is not None: # If new target is None
                if new_target.color == "black" and color == "black": 
                    #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites)) 
                    self.circle_king_cant_move.append((king_pos_x + 1, king_pos_y)) # Cant move here
                if new_target.color == "white" and color == "white": 
                    self.circle_white_king_cant_move.append((king_pos_x + 1, king_pos_y))
                    #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites)) 
            elif new_target is None: # If new target is the same color
                #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites)) 
                if color == "black":
                    self.circle_king_cant_move.append((king_pos_x + 1, king_pos_y)) # Cant move here
                elif color == "white":
                    self.circle_white_king_cant_move.append((king_pos_x + 1, king_pos_y))

        if 0 <= king_pos_x - 1 < 8 and 0 <= king_pos_y < 8: 
            new_target = self.board[king_pos_y][king_pos_x - 1]
            if new_target is not None: # If new target is None
                if new_target.color == "black" and color == "black": 
                    #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites)) 
                    self.circle_king_cant_move.append((king_pos_x - 1, king_pos_y)) # Cant move here
                if new_target.color == "white" and color == "white": 
                    self.circle_white_king_cant_move.append((king_pos_x -1, king_pos_y))
                    #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites)) 

            elif new_target is None: # If new target is the same color
                #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites)) 
                if color == "black":
                    self.circle_king_cant_move.append((king_pos_x - 1, king_pos_y)) # Cant move here
                elif color == "white":    
                    self.circle_white_king_cant_move.append((king_pos_x - 1, king_pos_y))

        # Bottom check
        for ex in range(king_pos_x - 1, king_pos_x + 2):
            if 0 <= ex < 8 and 0 <= king_pos_y + 1 < 8 : 
                new_target = self.board[king_pos_y + 1][ex]
                if new_target is not None: # If new target is None
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((ex, king_pos_y + 1)) # Cant move here
                    if new_target.color == "white" and color == "white": 
                        self.circle_white_king_cant_move.append((ex, king_pos_y + 1))
                        #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites)) 

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((ex, king_pos_y + 1)) # Cant move here
                    elif color == "white":
                        self.circle_white_king_cant_move.append((ex, king_pos_y + 1))

        # Top check
        for ex in range(king_pos_x - 1, king_pos_x + 2):
            if 0 <= ex < 8 and 0 <= king_pos_y - 1 < 8 :  
                new_target = self.board[king_pos_y - 1][ex]
                if new_target is not None: # If new target is None
                    if new_target.color == "black" and color == "black": # If new target is None
                        #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites)) 
                        self.circle_king_cant_move.append((ex, king_pos_y - 1)) # Cant move here
                    if new_target.color == "white" and color == "white": 
                        self.circle_white_king_cant_move.append((ex, king_pos_y - 1))
                        #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites)) 

                elif new_target is None: # If new target is the same color
                    #self.circles_ckeck.append(CircleCheck("brown", 5, (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites)) 
                    if color == "black":
                        self.circle_king_cant_move.append((ex, king_pos_y - 1)) # Cant move here
                    if color == "white":
                        self.circle_white_king_cant_move.append((ex, king_pos_y - 1))

    def check_king_check(self):
        """King checkmate check"""
        for j in range(8):
            for i in range(8):
                target = self.board[j][i] # If board has a piece
                if target is not None:
                    if target.piece_name == "rook.png":
                        self.check_king_rook_circles(j, i, target.color)  
                    if target.piece_name == "bishop.png":
                        self.check_king_bishop_circles(j, i, target.color)  
                    if target.piece_name == "queen.png":
                        self.check_king_bishop_circles(j, i, target.color) 
                        self.check_king_rook_circles(j, i, target.color)  
                    if target.piece_name == "knight.png":
                        self.check_king_knight_circle(j, i, target.color)
                    if target.piece_name == "pawn.png":
                       self.check_king_pawn_circle(j, i, target.color)
                    if target.piece_name == "king.png":
                        self.check_king_king_circle(j, i, target.color)

    def draw_king_circle(self):
        king_pos_x, king_pos_y  = self.rect_pos_x, self.rect_pos_y
        king_color = self.board[king_pos_y][king_pos_x].color
        
        print("King color", king_color)

        # Change postition king and rook
        if king_pos_x == 4 and (king_pos_y == 7 or king_pos_y == 0) and self.board[king_pos_y][king_pos_x].first_move == False:
            for x in range(1, 2): # Move to right if there is a rook
                if 0 <= king_pos_x + x < 8 and self.board[king_pos_y][king_pos_x + x] is None and self.board[king_pos_y][7].piece_name == "rook.png" and self.board[king_pos_y][7].color == king_color:
                    if king_color == "white" and x not in self.cant_move_king_can_be_checked_white_x_bishop and x not in self.cant_move_king_can_be_checked_white_x:
                        self.circles.append(Circle((SQUARE_SIZE * (king_pos_x + x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                    elif king_color == "black" and x not in self.bish and x not in self.cant_move_king_can_be_checked_black_x:
                        self.circles.append(Circle((SQUARE_SIZE * (king_pos_x + x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                else:
                    break
            for x_l in range(1, 2): # Move to left if there is a rook
                if 0 <= king_pos_x - x_l < 8 and self.board[king_pos_y][king_pos_x - x_l] is None and self.board[king_pos_y][0].piece_name == "rook.png" and self.board[king_pos_y][0].color == king_color:
                    if king_color == "white" and x_l not in self.cant_move_king_can_be_checked_white_x_bishop and x_l not in self.cant_move_king_can_be_checked_white_x:
                        self.circles.append(Circle((SQUARE_SIZE * (king_pos_x - x_l - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                    elif king_color == "black" and x_l not in self.cant_move_king_can_be_checked_black_x_bishop and x_l not in self.cant_move_king_can_be_checked_black_x:
                        self.circles.append(Circle((SQUARE_SIZE * (king_pos_x - x_l - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                else:
                    break

        # Side right and left
        if 0 <= king_pos_x + 1 < 8 : # No circles if thex are blue
            target = self.board[king_pos_y][king_pos_x + 1] 
            pos = (king_pos_x + 1, king_pos_y)
            if king_color == "white" and pos not in self.circle_king_cant_move: # Check if the list doenst contain these values
                if target is None: # Check None
                    self.circles.append(Circle((SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                if target is not None and king_color != target.color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
            if king_color == "black" and pos not in self.circle_white_king_cant_move: # Check if the list doenst contain these values
                if target is None: # Check None
                    self.circles.append(Circle((SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                if target is not None and king_color != target.color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))

        if 0 <= king_pos_x - 1 < 8 : 
            target = self.board[king_pos_y][king_pos_x - 1]
            pos = (king_pos_x - 1, king_pos_y) 
            if king_color == "white" and pos not in self.circle_king_cant_move: # When king white
                if  target is None: 
                    self.circles.append(Circle((SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                if target is not None and king_color != target.color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
            if king_color == "black" and pos not in self.circle_white_king_cant_move: # whne kine black
                if  target is None: 
                    self.circles.append(Circle((SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
                if target is not None and king_color != target.color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))

        # Bottom check
        for i in range(king_pos_x - 1, king_pos_x + 2):
            if 0 <= i < 8 and 0 <= king_pos_y + 1 < 8 : 
                target = self.board[king_pos_y + 1][i]
                pos = (i, king_pos_y + 1)
                if king_color == "white" and not pos in self.circle_king_cant_move:
                    if target is None: 
                        self.circles.append(Circle((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites))
                    if target is not None and king_color != target.color:
                        self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites))
                if king_color == "black" and not pos in self.circle_white_king_cant_move:
                    if target is None: 
                        self.circles.append(Circle((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites))
                    if target is not None and king_color != target.color:
                        self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites))

        # Top check
        for i in range(king_pos_x - 1, king_pos_x + 2):
            if 0 <= i < 8 and 0 <= king_pos_y - 1 < 8 :  
                target = self.board[king_pos_y - 1][i]
                pos = (i, king_pos_y - 1)
                if king_color == "white" and not pos  in self.circle_king_cant_move:
                    if target is None: 
                        self.circles.append(Circle((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites))
                    if target is not None and king_color != target.color:
                        self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites))
                if king_color == "black" and not pos  in self.circle_white_king_cant_move:
                    if target is None: 
                        self.circles.append(Circle((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites))
                    if target is not None and king_color != target.color:
                        self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites))
                
    def draw_queen_circle(self):
        self.draw_bishop_circle()
        self.draw_rook_circle()

    def draw_bishop_circle(self):
        """
        Draw the bish
        """
        # Check from y rect to 8
        # Circle for movement
        bishop_x = self.rect_pos_x
        bishop_y = self.rect_pos_y
        # Check down with postive x
        bishop_right_x = bishop_x

        condition_protect_x = bishop_right_x not in self.cant_move_king_can_be_checked_black_x if self.board[bishop_y][bishop_right_x].color == "black" else bishop_right_x not in self.cant_move_king_can_be_checked_white_x 
        condition_protect_y = bishop_y not in self.cant_move_king_can_be_checked_black_y if self.board[bishop_y][bishop_right_x].color == "black" else bishop_y not in self.cant_move_king_can_be_checked_white_y

        # Can kill the bishop or queen if it's near
        condition_protect_bishop_cant_move = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop)  

        condition_protect = condition_protect_x and condition_protect_y


        for i in range(bishop_y + 1, 8):
            bishop_right_x += 1
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, bishop_right_x) in self.position_king_checked))
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x] # Position where we are moving
                # Check enemy's bishop can check the king
                condition_protect_bishop = (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop)

                if target is not None and target.color == self.board[self.rect_pos_y][self.rect_pos_x].color: # if there is a piece with the same color
                    break  
                elif condition_to_move and condition_protect:
                    if condition_protect_bishop_cant_move: # Cant move if a bishop can check the king
                        if target is None :
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break
                    if condition_protect_bishop:
                        if target is None:
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break
                    
        # Check up with negative x
        bishop_right_x = bishop_x
        for i in range(bishop_y - 1, -1, -1):
            bishop_right_x -= 1
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, bishop_right_x) in self.position_king_checked))
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x]
                # Check enemy's bishop can check the king
                condition_protect_bishop = (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop)

                if target is not None and target.color == self.board[self.rect_pos_y][self.rect_pos_x].color: # if there is a piece with the same color
                    break  
                elif condition_to_move and condition_protect:
                    if condition_protect_bishop_cant_move:
                        if target is None:
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break
                    if condition_protect_bishop:
                        if target is None:
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break

        # Check down with native x
        bishop_right_x = bishop_x
        for i in range(bishop_y + 1, 8):
            bishop_right_x -= 1
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, bishop_right_x) in self.position_king_checked))
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                # Check enemy's bishop can check the king
                target = self.board[i][bishop_right_x]
                condition_protect_bishop = (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop)

                if target is not None and target.color == self.board[self.rect_pos_y][self.rect_pos_x].color: # if there is a piece with the same color
                    break  
                elif condition_to_move and  condition_protect:
                    if condition_protect_bishop_cant_move:
                        if target is None:
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break
                    if condition_protect_bishop:
                        if target is None:
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break

        # Check up with positive x
        bishop_right_x = bishop_x
        for i in range(bishop_y - 1, -1, -1):
            bishop_right_x += 1
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, bishop_right_x) in self.position_king_checked))
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x]
                # Check enemy's bishop can check the king
                condition_protect_bishop = (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (bishop_right_x, i) in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop)

                if target is not None and target.color == self.board[self.rect_pos_y][self.rect_pos_x].color: # if there is a piece with the same color
                    break  
                elif condition_to_move and condition_protect:
                    if condition_protect_bishop_cant_move: 
                        if target is None :
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break
                    if condition_protect_bishop:
                        if target is None:
                            self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        elif target is not None and target.color != self.board[self.rect_pos_y][self.rect_pos_x].color:
                            self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                            break # prevent next piece
                        else: break
            
    def draw_pawn_circle(self):     
        # Protect from bishop if it's near 
        condition_protect = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop)

        # Protect from rook if it's near
        condition_protect_rook = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x, self.cant_move_king_can_be_checked_black_y) if self.board[self.rect_pos_y][self.rect_pos_x].color == "black" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x, self.cant_move_king_can_be_checked_white_y)

        self.number_move_pawn = 2 if self.selected_piece.first_move else 3 # False == 2 moves
        # Move forward
        for i in range(self.rect_pos_y + self.move_direction, self.rect_pos_y + self.number_move_pawn * self.move_direction, self.move_direction):
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, self.rect_pos_x) in self.position_king_checked))
            if 0 <= i < 8 and 0 <= self.rect_pos_x < 8 and condition_to_move and self.board[i][self.rect_pos_x] is None and condition_protect: # Check if we have something in front of a pawn
                self.circles.append(Circle(((self.rect_pos_x + 0.5) * SQUARE_SIZE, ( i + 0.5 ) * SQUARE_SIZE ), self.group_sprites))
            else: break # If we have something in front of a pawn

        # enemy circle
        for i in range(self.rect_pos_x - 1, self.rect_pos_x + 2, 2):
            new_y = self.rect_pos_y + 1 * self.move_direction
            if 0 <= i < 8 and 0 <= new_y < 8 and ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((new_y, i) in self.position_king_checked)) and condition_protect_rook: # Check if we have something in front of a pawn
                target = self.board[new_y][i]
                if target is not None and target.color == self.enemy_color:
                    print(f"Enemy found at: ({i}, {new_y})")
                    self.circle_enemy.append(CircleEnemy(((i + 0.5) * SQUARE_SIZE, (new_y + 0.5) * SQUARE_SIZE), self.group_sprites))

    def draw_rook_circle(self):
        """
        Draws rook's circle to move towards and kill the enemy
        """
        # Check from y rect to 8
        for i in range(self.rect_pos_y + 1, 8):
            condition_protect = self.rect_pos_y not in self.cant_move_king_can_be_checked_white_y if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else self.rect_pos_y not in self.cant_move_king_can_be_checked_black_y
            
            condition_protect_bishop = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop)
            
            if 0 <= i < 8 and 0 <= self.rect_pos_x < 8 and  condition_protect and condition_protect_bishop:
                target = self.board[i][self.rect_pos_x]
                condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, self.rect_pos_x) in self.position_king_checked))
                if target is not None and target.color != self.enemy_color: # if there is a piece with the same color
                    break   
                elif condition_to_move:
                    if target == None: # Move only when there no piece between the enemy and the piece
                        self.circles.append(Circle(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    elif target is not None and target.color == self.enemy_color: # Check if the enemy
                        self.circle_enemy.append(CircleEnemy(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        break# When the rook see only one and then break
                    else:   
                        break # Cant move if there is the same piece color forward
        # Check from y rect to 0
        for i in range(self.rect_pos_y - 1, -1, -1):
            condition_protect = self.rect_pos_y not in self.cant_move_king_can_be_checked_white_y if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else self.rect_pos_y not in self.cant_move_king_can_be_checked_black_y

            condition_protect_bishop = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop)

            print(condition_protect)
            if 0 <= i < 8 and 0 <= self.rect_pos_x < 8 and condition_protect and condition_protect_bishop: # Or ((self.position_king_checked and self.position_king_checked[0][1] == self.rect_pos_x) 
                target = self.board[i][self.rect_pos_x]# Check if king is not checked
                condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((i, self.rect_pos_x) in self.position_king_checked))
                if target is not None and target.color != self.enemy_color: # if there is a piece with the same color
                    break   
                elif condition_to_move:
                    if target == None:
                        self.circles.append(Circle(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    elif target != None and target.color == self.enemy_color: # Check if the enemy
                        self.circle_enemy.append(CircleEnemy(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                        break # When the rook see only one and then break
                    else:   
                        break
                    
        # Check from x rect to 8
        for j in range(self.rect_pos_x + 1, 8):
            condition_protect = self.rect_pos_x not in self.cant_move_king_can_be_checked_white_x if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else self.rect_pos_x not in self.cant_move_king_can_be_checked_black_x
            
            condition_protect_bishop = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop)

            if 0 <= j < 8 and 0 <= self.rect_pos_y < 8 and ((self.position_king_checked and self.rect_pos_y == self.position_king_checked[0][0]) or (condition_protect and condition_protect_bishop)): # Check if king is not checked 
                target = self.board[self.rect_pos_y][j]
                condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((self.rect_pos_y, j) in self.position_king_checked))
                if target is not None and target.color != self.enemy_color: # if there is a piece with the same color
                    break  
                elif condition_to_move:
                    if target == None:
                        self.circles.append(Circle(((SQUARE_SIZE * (j + 0.5)), (self.rect_pos_y + 0.5) * SQUARE_SIZE ), self.group_sprites))
                    elif target != None and target.color == self.enemy_color: 
                        self.circle_enemy.append(CircleEnemy(((SQUARE_SIZE * (j + 0.5)), (self.rect_pos_y + 0.5) * SQUARE_SIZE  ), self.group_sprites))
                        break# When the rook see only one and then break
                    else:   
                        break

        # Check from x rect to 0
        for j in range(self.rect_pos_x - 1, -1, -1):
            condition_protect = self.rect_pos_x not in self.cant_move_king_can_be_checked_white_x if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else self.rect_pos_x not in self.cant_move_king_can_be_checked_black_x

            condition_protect_bishop = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop)

            if 0 <= j < 8 and 0 <= self.rect_pos_y < 8 and ((self.position_king_checked and self.rect_pos_y == self.position_king_checked[0][0]) or (condition_protect and condition_protect_bishop)): # Check if king is not checked 
                target = self.board[self.rect_pos_y][j]
                condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((self.rect_pos_y, j) in self.position_king_checked))
                if target is not None and target.color != self.enemy_color: # if there is a piece with the same color
                    break  
                elif condition_to_move:
                    if target == None:
                        self.circles.append(Circle(((SQUARE_SIZE * (j + 0.5)), (self.rect_pos_y + 0.5) * SQUARE_SIZE  ), self.group_sprites))
                    elif target != None and target.color == self.enemy_color: # Check if the enemy
                        self.circle_enemy.append(CircleEnemy(((SQUARE_SIZE * (j + 0.5)), (self.rect_pos_y + 0.5) * SQUARE_SIZE  ), self.group_sprites))
                        break
                    else:   
                        break
        # Enemy circles

    def _draw_knight_circles_x(self, i, knight_y_pos):
        """Draws circles on y"""
        condition_protect = ((self.rect_pos_x not in self.cant_move_king_can_be_checked_white_x) and (self.rect_pos_y not in self.cant_move_king_can_be_checked_white_y)) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else ((self.rect_pos_x not in self.cant_move_king_can_be_checked_black_x) and (self.rect_pos_y not in self.cant_move_king_can_be_checked_black_y)) 

        condition_protect_bishop = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop)

        if  0 <= i < 8 and condition_protect and condition_protect_bishop: # Check forward y +
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((knight_y_pos + 2, i) in self.position_king_checked))
            # If the king can be checked
            if 0 <= knight_y_pos + 2 < 8 and condition_to_move : 
                target = self.board[knight_y_pos + 2][i]
                if target == None: # Check new pos == None
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 2 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 2 + 0.5))), self.group_sprites))
            
            condition_to_move_2 = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((knight_y_pos - 2, i) in self.position_king_checked))
            if  0 <= knight_y_pos - 2 < 8 and condition_to_move_2 and condition_protect_bishop:
                target = self.board[knight_y_pos - 2][i]
                if target == None:
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos - 2 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos - 2 + 0.5))), self.group_sprites))
        
    def _draw_knight_circles_y(self, i, knight_y_pos):
        """Draws circles on y"""
        condition_protect = ((self.rect_pos_x not in self.cant_move_king_can_be_checked_white_x) and (self.rect_pos_y not in self.cant_move_king_can_be_checked_white_y)) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else ((self.rect_pos_x not in self.cant_move_king_can_be_checked_black_x) and (self.rect_pos_y not in self.cant_move_king_can_be_checked_black_y)) 

        condition_protect_bishop = (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_white_x_bishop, self.cant_move_king_can_be_checked_white_y_bishop) if self.board[self.rect_pos_y][self.rect_pos_x].color == "white" else (self.rect_pos_x, self.rect_pos_y) not in zip(self.cant_move_king_can_be_checked_black_x_bishop, self.cant_move_king_can_be_checked_black_y_bishop)

        if 0 <= i < 8 and condition_protect and condition_protect_bishop: # check right x +
            condition_to_move = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((knight_y_pos + 1, i) in self.position_king_checked))
            if 0 <= knight_y_pos + 1 < 8 and condition_to_move: 
                target = self.board[knight_y_pos + 1][i]
                if target == None:
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 1 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 1 + 0.5))), self.group_sprites))
                    
            condition_to_move_2 = ((not self.cant_move_black_pieces and not self.cant_move_white_pieces) or ((knight_y_pos - 1, i) in self.position_king_checked))
            if 0 <= knight_y_pos - 1 < 8 and condition_to_move_2 and condition_protect_bishop: 
                target = self.board[knight_y_pos - 1][i]
                if target == None:
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos - 1 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos - 1 + 0.5))), self.group_sprites))
    
    def draw_knight_circle(self):  
        # Check from y rect to x + 1
        knight_x_pos = self.rect_pos_x
        knight_y_pos = self.rect_pos_y 
        
        for i in range(knight_x_pos + 1, knight_x_pos + 2):
            self._draw_knight_circles_x(i, knight_y_pos)

        for i in range(knight_x_pos + 2, knight_x_pos + 3):
            self._draw_knight_circles_y(i, knight_y_pos)

        # Check from y rect to x - 1
        for i in range(knight_x_pos - 1, knight_x_pos - 2,  -1): 
            self._draw_knight_circles_x(i, knight_y_pos)

        for i in range(knight_x_pos - 2, knight_x_pos - 3, -1):
            self._draw_knight_circles_y(i, knight_y_pos)

    def check_pawn_into_queen(self):         
        # Change pawn when it reaches the top
        if self.piece_name == "pawn":
            for i in range(8):
                if self.selected_piece.color == "white" and self.board[0][i] == self.selected_piece:
                    self.selected_piece.kill()
                    self.board[0][i] = Piece(join("img", "white", "queen.png"), 
                                    (self.dash_left + SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (0.5)), # Dash bottom !!!!!
                                    "white", "queen.png", 
                                    (self.group_sprites, self.piece_group, self.black_group))
                    print("White change")
                elif self.selected_piece.color == "black" and self.board[7][i] == self.selected_piece:
                    self.selected_piece.kill()
                    self.board[7][i] = Piece(join("img", "black", "queen.png"), 
                                    (self.dash_left + SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (7.5)), 
                                    "black", "queen.png", 
                                    (self.group_sprites, self.piece_group, self.black_group))

    def check_piece_movement(self, square_position_y, square_position_x, rect_pos_y, rect_pos_x):
        """Checks pawns movement"""
        for circle in self.circles:
            self.circle_x = circle.rect.centerx // SQUARE_SIZE # Pos of a circle in the list circles and the board 
            self.circle_y = circle.rect.centery // SQUARE_SIZE

            if square_position_x == self.circle_x and square_position_y == self.circle_y and self.board[square_position_y][square_position_x] == None: # If circle == square_position
                if self.selected_piece.piece_name == "king.png" and self.board[self.rect_pos_y][4] is not None and self.board[self.rect_pos_y][4].piece_name == "king.png":
                    if square_position_x == 6 and self.board[self.rect_pos_y][7].piece_name == "rook.png" and self.board[self.rect_pos_y][7].color == self.board[self.rect_pos_y][4].color:
                        self.board[self.rect_pos_y][7].move_piece(5, square_position_y) # Move rook to castling
                        self.board[self.rect_pos_y][5] = self.board[self.rect_pos_y][7] 
                        self.board[self.rect_pos_y][7] = None 
                    if square_position_x == 2 and self.board[self.rect_pos_y][0].piece_name == "rook.png" and self.board[self.rect_pos_y][0].color == self.board[self.rect_pos_y][4].color:
                        self.board[self.rect_pos_y][0].move_piece(3, square_position_y) # Move rook to castling
                        self.board[self.rect_pos_y][3] = self.board[self.rect_pos_y][0] 
                        self.board[self.rect_pos_y][0] = None 
                        

                self.enemy_color = "white" if self.enemy_color == "black" else "black" # Checks enemy's color
                self.selected_piece.move_piece(square_position_x, square_position_y)
                print(f"Move! {self.selected_piece.piece_name}")
                self.selected_piece.first_move = True # Checks first move
                print(self.selected_piece.piece_name)
                # Change postions in board list
                self.change_board_position(square_position_y, square_position_x, rect_pos_y, rect_pos_x)

                self.piece_color_move = not self.piece_color_move # Change the color to move
                

                self.delete_cirlce_check() # Delete previous circles
                self.check_pawn_into_queen()

                self.king_is_not_checked() # When move than set check can move cirles To False
                self.add_pos_check_can_move(square_position_x, square_position_y) # Pos can move to protect the king
                print("Piece check pos ", self.position_king_checked)
        
        # Attack the  Enemy    
        for circle in self.circle_enemy:
            self.circle_x_enemy = circle.rect.centerx // SQUARE_SIZE # Pos of a circle in the list circles and the board 
            self.circle_y_enemy = circle.rect.centery // SQUARE_SIZE

            if square_position_x == self.circle_x_enemy and square_position_y == self.circle_y_enemy: # If circle == square_position
                print("Enemy", self.circle_x_enemy, self.circle_y_enemy)
                self.enemy_color = "white" if self.enemy_color == "black" else "black" # Checks enemy's color
                enemy_kill = self.board[square_position_y][square_position_x]
                print(f"Kill! {enemy_kill.piece_name}")
                enemy_kill.kill() # Kill the sprite
                enemy_kill = None # Clear the board
                self.change_board_position(square_position_y, square_position_x, rect_pos_y, rect_pos_x) # Change on the board
                self.selected_piece.move_piece(square_position_x, square_position_y)
                # Change a pawn into a queen
                self.check_pawn_into_queen()
                self.delete_cirlce_check() # Delete previous circles
                self.piece_color_move = not self.piece_color_move # Change the color to move
                

                self.king_is_not_checked() # When move than To False
                self.add_pos_check_can_move(square_position_x, square_position_y)
                print("Piece check pos ", self.position_king_checked)

        self.move_is_over = True # Cant move anymore the selected piece
        self.selected_piece = None # None selected
        
    def check_movement(self, mouse_pos):
        """Check if the piece can move"""
        if self.selected_piece and not self.move_is_over:
            square_position_y = mouse_pos[1] // SQUARE_SIZE # Shows the rows
            square_position_x = mouse_pos[0] // SQUARE_SIZE # Shows the columns
            print("Piece check pos before ", self.position_king_checked)
            print("Square pos ", square_position_y, square_position_x)
            print("King can be checked black x", self.cant_move_king_can_be_checked_black_x)
            print("King can be checked black y", self.cant_move_king_can_be_checked_black_y)
            print("King can be checked white x", self.cant_move_king_can_be_checked_white_x)
            print("King can be checked white y", self.cant_move_king_can_be_checked_white_y)
            print("King can be checked black x bishop", self.cant_move_king_can_be_checked_black_x_bishop)
            print("King can be checked black y bishop", self.cant_move_king_can_be_checked_black_y_bishop)
            print("King can be checked white x bishop", self.cant_move_king_can_be_checked_white_x_bishop)
            print("King can be checked white y bishop", self.cant_move_king_can_be_checked_white_y_bishop)

            # Checks if we can move when there is None in the next square 
            if 0 <= square_position_x < 8 and 0 <= square_position_y < 8 :  # Check if it mouse pos 0 <= pos <= 7 
                
                self.check_piece_movement(square_position_y, square_position_x, self.rect_pos_y, self.rect_pos_x)
                self.add_pos_can_be_checked()
            # print(self.board)

            # Delete all circles
            self.delete_circles()

    def delete_pos_can_be_checked_black(self):
        """
        This function kills any existing circles indicating positions where the king cannot be moved. Only black
        """
        # Kill circles (delete later)
        for circle in self.cant_move_king_can_be_checked_circles:
            circle.kill()
        self.cant_move_king_can_be_checked_circles.clear()

        # Clear all x and y positions
        self.cant_move_king_can_be_checked_black_x.clear()
        self.cant_move_king_can_be_checked_black_y.clear()

    def delete_pos_can_be_checked_white(self):
        """
        This function kills any existing circles indicating positions where the king cannot be moved. Only white
        """
        # Kill circles (delete later)
        for circle in self.cant_move_king_can_be_checked_circles:
            circle.kill()
        self.cant_move_king_can_be_checked_circles.clear()
        self.cant_move_king_can_be_checked_white_x.clear()
        self.cant_move_king_can_be_checked_white_y.clear()

    def delete_pos_can_be_checked_black_bishop(self):
        """
        deletes bishops and queen positions where the king cannot be moved
        """
        self.cant_move_king_can_be_checked_black_x_bishop.clear()
        self.cant_move_king_can_be_checked_black_y_bishop.clear()

    def delete_pos_can_be_checked_white_bishop(self):
        """
        deletes bishops and queen positions where the king cannot be moved
        """
        self.cant_move_king_can_be_checked_white_x_bishop.clear()
        self.cant_move_king_can_be_checked_white_y_bishop.clear()

    def add_pos_can_be_checked(self):
        """
        This function finds the positions of rooks and queens, and checks if the king can be checked by them.
        It also kills any existing circles indicating positions where the king cannot be moved.
        """
        rook_y_count_black, rook_y_count_white = 0, 0 # Count when we have two before between the king and rook enemy 
        rook_x_count_black, rook_x_count_white = 0, 0 # Count when we have two before between the king and rook enemy  
        bishop_count_black, bishop_count_white = 0, 0 # Count when we have two before between the king and rook enemy  
        for j in range(8):
            for i in range(8):
                king = self.board[j][i]
                if king is not None and king.piece_name == "king.png" and king.color != self.enemy_color:
                    print(f"King = {j} and {i}")
                    # if there is no enemy in the front
                    self.delete_pos_can_be_checked_black() # Refresh pos after a certain move
                    self.delete_pos_can_be_checked_white()
                    
                    self.delete_pos_can_be_checked_black_bishop() # Refresh pos after a certain move
                    self.delete_pos_can_be_checked_white_bishop() # Refresh pos after a certain move
                    # Check if the king is in check by bishop
                  
                    for y in range(8):
                        for x in range(8):
                            if self.board[y][x] is not None and self.board[y][x].piece_name in ["bishop.png", "queen.png"] and self.board[y][x].color == self.enemy_color and king.color != self.enemy_color:

                                dif_y = j - y # Difference between king and bishop
                                dif_x = i - x
                                if (dif_y != 0 and dif_x != 0) and (abs(dif_y) == abs(dif_x)): 
                                    step_y = 1 if dif_y > 0 else -1
                                    step_x = 1 if dif_x > 0 else -1

                                        # Add the bishop or queen into the list in order to kill them by enemy bishop or queen
                                    if king.color == "white":
                                        if self.board[y][x].color != "white":
                                            self.cant_move_king_can_be_checked_white_x_bishop.append(x)
                                            self.cant_move_king_can_be_checked_white_y_bishop.append(y)
                                    elif king.color == "black":
                                        if self.board[y][x].color != "black":
                                            self.cant_move_king_can_be_checked_black_x_bishop.append(x)
                                            self.cant_move_king_can_be_checked_black_y_bishop.append(y)

                                    for d in range(1, abs(dif_y)):
                                        self.cant_move_king_can_be_checked_circles.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i - d * step_x + 0.5), SQUARE_SIZE * (j - d * step_y+ 0.5)), self.group_sprites))
                                        if 0 <= x+d*step_x  < 8 and 0 <= y+d*step_y < 8:
                                            target = self.board[y+d*step_y][x+d*step_x]
                                            if king.color == "white":
                                                if target is not None and target.color == "white":
                                                    self.cant_move_king_can_be_checked_white_x_bishop.append(x+d*step_x)
                                                    self.cant_move_king_can_be_checked_white_y_bishop.append(y+d*step_y)
                                                    bishop_count_white += 1
                                                    if bishop_count_white > 1:
                                                        self.cant_move_king_can_be_checked_white_x_bishop.clear()
                                                        self.cant_move_king_can_be_checked_white_y_bishop.clear()
                                                elif target is None:
                                                    self.cant_move_king_can_be_checked_white_x_bishop.append(x+d*step_x)
                                                    self.cant_move_king_can_be_checked_white_y_bishop.append(y+d*step_y)
                                            if king.color == "black":
                                                if target is not None and target.color == "black":
                                                    self.cant_move_king_can_be_checked_black_x_bishop.append(x+d*step_x)
                                                    self.cant_move_king_can_be_checked_black_y_bishop.append(y+d*step_y)
                                                    bishop_count_black += 1
                                                    if bishop_count_black > 1:
                                                        self.cant_move_king_can_be_checked_black_x_bishop.clear()
                                                        self.cant_move_king_can_be_checked_black_y_bishop.clear()
                                                   
                                                elif target is None:
                                                    self.cant_move_king_can_be_checked_black_x_bishop.append(x+d*step_x)
                                                    self.cant_move_king_can_be_checked_black_y_bishop.append(y+d*step_y)
                            if self.board[y][x] is not None and self.board[y][x].piece_name in ["rook.png", "queen.png"] and self.board[y][x].color == self.enemy_color and king.color != self.enemy_color:

                                dif_y = j - y # Difference between king and bishop
                                dif_x = i - x

                                if (dif_x == 0 and dif_y != 0): 
                                    step_y = 1 if dif_y > 0 else -1
                                    for d in range(1, abs(dif_y)):
                                        self.cant_move_king_can_be_checked_circles.append(CircleCheck("blue", 10, (SQUARE_SIZE * (x + 0.5), SQUARE_SIZE * (y + d * step_y+ 0.5)), self.group_sprites))
                                        if 0 <= y+d*step_y < 8:
                                            target = self.board[y+d*step_y][x]
                                            if king.color == "white":
                                                if target is not None and target.color == "white":
                                                    self.cant_move_king_can_be_checked_white_y.append(y+d*step_y)
                                                    rook_y_count_white += 1
                                                    print(f"Rool count ", rook_y_count_white)
                                                    if rook_y_count_white > 1:
                                                        self.cant_move_king_can_be_checked_white_y.clear() # Refresh pos if there is two figures
                                                        rook_y_count_white = 0 # Count when we have two before between the rook and rook enemy
                                                    #break
                                                elif target is None:
                                                    self.cant_move_king_can_be_checked_white_y.append(y+d*step_y)
                                            if king.color == "black":
                                                if target is not None and target.color == "black":
                                                    self.cant_move_king_can_be_checked_black_y.append(y+d*step_y)
                                                    rook_y_count_black += 1
                                                    if rook_y_count_black > 1:
                                                        self.cant_move_king_can_be_checked_black_y.clear() # Refresh pos if there is two figures
                                                        rook_y_count_black = 0
                                                elif target is None:
                                                    self.cant_move_king_can_be_checked_black_y.append(y+d*step_y)

                                elif (dif_y == 0 and dif_x != 0): 
                                    step_x = 1 if dif_x > 0 else -1
                                    for d in range(1, abs(dif_x)):
                                        self.cant_move_king_can_be_checked_circles.append(CircleCheck("blue", 10, (SQUARE_SIZE * (x + d * step_x + 0.5), SQUARE_SIZE * (y+ 0.5)), self.group_sprites))
                                        if 0 <= x+d*step_x  < 8:
                                            target = self.board[y][x+d*step_x]
                                            if king.color == "white":
                                                if target is not None and target.color == "white":
                                                    self.cant_move_king_can_be_checked_white_x.append(x+d*step_x)
                                                    rook_x_count_white += 1
                                                    print(f"Rool count ", rook_x_count_white)
                                                    if rook_x_count_white > 1:
                                                        self.cant_move_king_can_be_checked_white_x.clear() # Refresh pos if there is two figures
                                                        rook_x_count_white = 0 # Count when we have two before between the rook and rook enemy
                                                    #break
                                                elif target is None:
                                                    self.cant_move_king_can_be_checked_white_x.append(x+d*step_x)
                                            if king.color == "black":
                                                if target is not None and target.color == "black":
                                                    self.cant_move_king_can_be_checked_black_x.append(x+d*step_x)
                                                    rook_x_count_black += 1
                                                    if rook_x_count_black > 1:
                                                        self.cant_move_king_can_be_checked_black_x.clear() # Refresh pos if there is two figures
                                                        rook_x_count_black = 0
                                                elif target is None:
                                                    self.cant_move_king_can_be_checked_black_x.append(x+d*step_x)

    def add_pos_check_can_move(self, square_position_x, square_position_y):
        """Adds positions where a piece can protect the king"""
        if self.board[square_position_y][square_position_x] is not None and self.board[square_position_y][square_position_x].color == self.enemy_color:
            self.position_king_checked.append((square_position_y, square_position_x)) # Pos when a king is checked
        for j in range(8):
            for i in range(8):
                king = self.board[j][i]
                if king is not None and king.piece_name == "king.png" and king.color != self.enemy_color:
                    # Find the difference with abs
                    dif_x = square_position_x - i
                    dif_y = square_position_y - j
                    print(f"Diff x = {dif_x}, diff y = {dif_y}")
                    if dif_x == 0: # If x == x
                        step_y = 1 if dif_y > 0 else -1
                        for d_y in range(step_y, dif_y, step_y): 
                            self.cant_move_king_can_be_checked_circles.append(CircleCheck("green", 10, (SQUARE_SIZE * (square_position_x + 0.5), SQUARE_SIZE * (d_y + j+ 0.5)), self.group_sprites))
                            self.position_king_checked.append((d_y + j, square_position_x))
                    
                    elif dif_y == 0: # If y == y
                        step_x = 1 if dif_x > 0 else -1
                        for d_x in range(step_x, dif_x, step_x):
                            #self.cant_move_king_can_be_checked_circles.append(CircleCheck("red", 20, (SQUARE_SIZE * (d_x + i + 0.5), SQUARE_SIZE * (square_position_y + 0.5)), self.group_sprites))
                            self.position_king_checked.append((square_position_y, d_x + i))      

                    elif dif_x != 0 and dif_y != 0:
                        step_y = 1 if dif_y > 0 else -1
                        step_x = 1 if dif_x > 0 else -1
                        for d in range(1, abs(dif_y)):
                            #self.cant_move_king_can_be_checked_circles.append(CircleCheck("blue", 10, (SQUARE_SIZE * (i + d * step_x + 0.5), SQUARE_SIZE * (j + d * step_y+ 0.5)), self.group_sprites))
                            self.position_king_checked.append((j + d * step_y, i + d * step_x))
                                     
    def delete_circles(self):
        """Delete all circles after a movement"""    
        for circle in self.circles:
            circle.kill()   

        for circle in self.circle_enemy:
            circle.kill()   

        self.circles.clear()
        self.circle_enemy.clear()   

    def delete_cirlce_check(self):
        """Deletes the checkmate circles"""
        for circle in self.circles_ckeck:
            circle.kill()   

        self.circle_king_cant_move.clear()
        self.circle_white_king_cant_move.clear()
        self.circles_ckeck.clear()   
        
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
                                         (self.group_sprites, self.piece_group, self.black_group))

        for j in range(2):
            for i in range(8):
                self.board[j+6][i] = Piece(join("img", "white", self.white_images[j][i]), 
                                         (self.dash_left + SQUARE_SIZE * (i + 0.5), self.dash_top + SQUARE_SIZE * (j + 6.5)), 
                                         "white", self.white_images[j][i], 
                                         (self.group_sprites, self.piece_group, self.white_group))
        
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
