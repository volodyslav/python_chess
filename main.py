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
        self.circles_ckeck = []

        # fOR MOVING
        self.selected_piece = None
        self.move_is_over = False

        self.can_move = False # Check if nothing between piece and square to move 

        self.piece_color_move = True # Check color before moving
        # Circles for movement
        self.circles = [] 
        # Circles for beating
        self.circle_enemy = []
        
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

                    self.enemy_color = "white" if self.piece_color == "black" else "black" # Checks enemy's color

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


    def check_king_check(self):
        for j in range(8):
            for i in range(8):
                king_pos = self.board[j][i] # King position 
                if king_pos is not None and king_pos.piece_name == 'king.png' and king_pos.color == "black":
                    king_pos_x = i # Pos x
                    king_pos_y = j # Pos y
                    king_color = king_pos.color # king color
                    enemy_color = "black" if king_color == "white" else "white" # enemy color
                    print("King: ", king_pos_y, king_pos_x)
                    # iter to find the enemy
                    for ey in range(king_pos_y + 1, 8): # From king to bottom
                        for ex in range(king_pos_x - 1, king_pos_x + 2): # x- 1 to x + 1
                            if 0 <= ey < 8 and 0 <= ex < 8: 
                                if self.board[ey][ex] is not None and self.board[ey][ex].color == "black":
                                    break
                                elif self.board[ey][ex] is not None and self.board[ey][ex].color == "white" :
                                    self.circles_ckeck.append(CircleCheck("blue", (SQUARE_SIZE * (ex + 0.5), SQUARE_SIZE * (ey + 0.5)), self.group_sprites)) 
                       
                       

    def draw_king_circle(self):
        king_pos_x = self.rect_pos_x
        king_pos_y = self.rect_pos_y

        # Side right and left
        if 0 <= king_pos_x + 1 < 8:
            target = self.board[king_pos_y][king_pos_x + 1]
            if target is None: # Check None
                self.circles.append(Circle((SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
            elif target != None and target.color == self.enemy_color:
                self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (king_pos_x + 1.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))

        if 0 <= king_pos_x - 1 < 8: 
            target = self.board[king_pos_y][king_pos_x - 1]
            if  target == None: 
                self.circles.append(Circle((SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))
            elif target != None and target.color == self.enemy_color:
                self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (king_pos_x - 0.5), SQUARE_SIZE * (king_pos_y + 0.5)), self.group_sprites))

        # Bottom check
        for i in range(king_pos_x - 1, king_pos_x + 2):
            if 0 <= i < 8 and 0 <= king_pos_y + 1 < 8: 
                target = self.board[king_pos_y + 1][i]
                if target == None: 
                    self.circles.append(Circle((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites))
                elif target != None and target.color == self.enemy_color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y + 1.5)), self.group_sprites))

        # Top check
        for i in range(king_pos_x - 1, king_pos_x + 2):
            if 0 <= i < 8 and 0 <= king_pos_y - 1 < 8: 
                target = self.board[king_pos_y - 1][i]
                if target == None: 
                    self.circles.append(Circle((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites))
                elif target != None and target.color == self.enemy_color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (i + 0.5), SQUARE_SIZE * (king_pos_y - 0.5)), self.group_sprites))
            
    def draw_queen_circle(self):
        self.draw_bishop_circle()
        self.draw_rook_circle()

    def draw_bishop_circle(self):
        # Check from y rect to 8
        # Circle for movement
        bishop_x = self.rect_pos_x
        bishop_y = self.rect_pos_y
        # Check down with postive x
        bishop_right_x = bishop_x
        for i in range(bishop_y + 1, 8):
            bishop_right_x += 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x]
                if target == None:
                    self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    break # prevent next piece
                else: break

        # Check up with negative x
        bishop_right_x = bishop_x
        for i in range(bishop_y - 1, -1, -1):
            bishop_right_x -= 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x]
                if target == None:
                    self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    break # prevent next piece
                else: break

        # Check down with native x
        bishop_right_x = bishop_x
        for i in range(bishop_y + 1, 8):
            bishop_right_x -= 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x]
                if target == None:
                    self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    break # prevent next piece
                else: break

        # Check up with positive x
        bishop_right_x = bishop_x
        for i in range(bishop_y - 1, -1, -1):
            bishop_right_x += 1
            if 0 <= bishop_right_x < 8 and 0 <= i < 8: 
                target = self.board[i][bishop_right_x]
                if target == None:
                    self.circles.append(Circle((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color:
                    self.circle_enemy.append(CircleEnemy((SQUARE_SIZE * (bishop_right_x + 0.5), (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    break # prevent next piece
                else: break
            
        # Draw Cirlces for Eneny position
        
    def draw_pawn_circle(self):     
        self.number_move_pawn = 2 if self.selected_piece.first_move else 3 # False == 2 moves
        for i in range(self.rect_pos_y + self.move_direction, self.rect_pos_y + self.number_move_pawn * self.move_direction, self.move_direction):
            if 0 <= i < 8 and self.board[i][self.rect_pos_x] == None: # Check if we have something in front of a pawn
                self.circles.append(Circle(((self.rect_pos_x + 0.5) * SQUARE_SIZE, ( i + 0.5 ) * SQUARE_SIZE ), self.group_sprites))
            
        # enemy circle
        for i in range(self.rect_pos_x - 1, self.rect_pos_x + 2, 2):
            new_y = self.rect_pos_y + 1 * self.move_direction
            if 0 <= i < 8 and 0 <= new_y < 8:
                target = self.board[new_y][i]
                if target is not None and target.color == self.enemy_color:
                    print(f"Enemy found at: ({i}, {new_y})")
                    self.circle_enemy.append(CircleEnemy(((i + 0.5) * SQUARE_SIZE, (new_y + 0.5) * SQUARE_SIZE), self.group_sprites))

    def draw_rook_circle(self):
        # Check from y rect to 8
        for i in range(self.rect_pos_y + 1, 8):
            if 0 <= i < 8:
                target = self.board[i][self.rect_pos_x]
                if target == None:
                    self.circles.append(Circle(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if the enemy
                    self.circle_enemy.append(CircleEnemy(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                    break# When the rook see only one and then break
                else:   
                    break # Cant move if there is the same piece color forward
        # Check from y rect to 0
        for i in range(self.rect_pos_y - 1, -1, -1):
            if 0 <= i < 8:  
                target = self.board[i][self.rect_pos_x]
                if target == None:
                    self.circles.append(Circle(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if the enemy
                    self.circle_enemy.append(CircleEnemy(((self.rect_pos_x + 0.5) * SQUARE_SIZE, (SQUARE_SIZE * (i + 0.5))), self.group_sprites))

                    break # When the rook see only one and then break
                else:   
                    break
        # Check from x rect to 8
        for j in range(self.rect_pos_x + 1, 8):
            if 0 <= j < 8:
                target = self.board[self.rect_pos_y][j]
                if target == None:
                    self.circles.append(Circle(((SQUARE_SIZE * (j + 0.5)), (self.rect_pos_y + 0.5) * SQUARE_SIZE ), self.group_sprites))
                elif target != None and target.color == self.enemy_color: 
                    self.circle_enemy.append(CircleEnemy(((SQUARE_SIZE * (j + 0.5)), (self.rect_pos_y + 0.5) * SQUARE_SIZE  ), self.group_sprites))
                    break# When the rook see only one and then break
                else:   
                    break
        # Check from x rect to 0
        for j in range(self.rect_pos_x - 1, -1, -1):
            if 0 <= j < 8: 
                target = self.board[self.rect_pos_y][j]
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
        if  0 <= i < 8: # Check forward y +
            if 0 <= knight_y_pos + 2 < 8: # Checks if new 0< = y < 8 
                target = self.board[knight_y_pos + 2][i]
                if target == None: # Check new pos == None
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 2 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 2 + 0.5))), self.group_sprites))
            
            if  0 <= knight_y_pos - 2 < 8:
                target = self.board[knight_y_pos - 2][i]
                if target == None:
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos - 2 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos - 2 + 0.5))), self.group_sprites))
        
    def _draw_knight_circles_y(self, i, knight_y_pos):
        """Draws circles on y"""
        if 0 <= i < 8: # check right x +
            if 0 <= knight_y_pos + 1 < 8: 
                target = self.board[knight_y_pos + 1][i]
                if target == None:
                    self.circles.append(Circle((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 1 + 0.5))), self.group_sprites))
                elif target != None and target.color == self.enemy_color: # Check if we have enemy on new pos
                    self.circle_enemy.append(CircleEnemy((( SQUARE_SIZE * (i + 0.5)), (SQUARE_SIZE * (knight_y_pos + 1 + 0.5))), self.group_sprites))
                    
            if 0 <= knight_y_pos - 1 < 8: 
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
                self.selected_piece.move_piece(square_position_x, square_position_y)
                print(f"Move! {self.selected_piece.piece_name}")
                self.selected_piece.first_move = True # Checks first move
                print(self.selected_piece.piece_name)
                # Change postions in board list
                self.change_board_position(square_position_y, square_position_x, rect_pos_y, rect_pos_x)

                self.piece_color_move = not self.piece_color_move # Change the color to move

                self.check_king_check() # check ckeck or ckeckmate

                self.check_pawn_into_queen()

        # Attack the  Enemy    
        for circle in self.circle_enemy:
            self.circle_x_enemy = circle.rect.centerx // SQUARE_SIZE # Pos of a circle in the list circles and the board 
            self.circle_y_enemy = circle.rect.centery // SQUARE_SIZE

            if square_position_x == self.circle_x_enemy and square_position_y == self.circle_y_enemy: # If circle == square_position
                print("Enemy", self.circle_x_enemy, self.circle_y_enemy)
                enemy_kill = self.board[square_position_y][square_position_x]
                print(f"Kill! {enemy_kill.piece_name}")
                enemy_kill.kill() # Kill the sprite
                enemy_kill = None # Clear the board
                self.change_board_position(square_position_y, square_position_x, rect_pos_y, rect_pos_x) # Change on the board
                self.selected_piece.move_piece(square_position_x, square_position_y)
                # Change a pawn into a queen
                self.check_pawn_into_queen()

                self.piece_color_move = not self.piece_color_move # Change the color to move

                

        self.move_is_over = True # Cant move anymore the selected piece
        self.selected_piece = None # None selected


    def check_movement(self, mouse_pos):
        """Check if the piece can move"""
        if self.selected_piece and not self.move_is_over:
            square_position_y = mouse_pos[1] // SQUARE_SIZE # Shows the rows
            square_position_x = mouse_pos[0] // SQUARE_SIZE # Shows the columns
            print("Square pos ", square_position_y, square_position_x)
            # Checks if we can move when there is None in the next square 
            if 0 <= square_position_x < 8 and 0 <= square_position_y < 8 :  # Check if it mouse pos 0 <= pos <= 7 
                self.check_piece_movement(square_position_y, square_position_x, self.rect_pos_y, self.rect_pos_x)
            
            # print(self.board)
            # Delete all circles
            self.delete_circles()
            
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
