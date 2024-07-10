from settings import *
from piece import *
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
        self.dash_left = self.rect_dashboard.left
        # All group
        self.group_sprites = pygame.sprite.Group()

        # Black  and white groups
        self.black_group = pygame.sprite.Group()
        self.white_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        
        self.selected_piece = False

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    print(mouse_pos)
                    square_position_y =  mouse_pos[1] // SQUARE_SIZE[1] # Shows the rows
                    square_position_x = mouse_pos[0] // SQUARE_SIZE[0] # Shows the rows
                    print(square_position_y, square_position_x)
                    for piece in self.group_sprites:
                        if not self.selected_piece and piece.rect.collidepoint(mouse_pos):
                            self.selected_piece = True
                            print(f"{piece.piece_name} - {piece.color}")
                            rect_pos_y = int(piece.rect.y // SQUARE_SIZE[1])
                            rect_pos_x = int(piece.rect.x // SQUARE_SIZE[1])
                            print(rect_pos_y, rect_pos_x)
                            if rect_pos_y != square_position_y: # Check if doesn't choose the same piece
                                self.board[square_position_y][square_position_x] = self.board[rect_pos_y][rect_pos_x] 
                                self.board[rect_pos_y][rect_pos_x] = None
                            #print(self.board)
                            
                                 
                    self.selected_piece = False
                    
            self.show_screen()
            self.draw_board_pieces()


    def draw_board_pieces(self):
        """Draw the pieces on the screen"""
        for j in range(2):
            for i in range(8):
                self.board[j][i] = Piece(join("img", "black", self.black_images[j][i]), 
                                         (self.dash_left + SQUARE_SIZE[0] * (i + 0.5), SQUARE_SIZE[1] * (j + 1)), 
                                          "black", self.black_images[j][i], 
                                         (self.group_sprites, self.black_group))

        for j in range(2):
            for i in range(8):
                self.board[j+6][i] = Piece(join("img", "white", self.white_images[j][i]), 
                                         (self.dash_left + SQUARE_SIZE[0] * (i + 0.5), SQUARE_SIZE[1] * (j + 7)), 
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
