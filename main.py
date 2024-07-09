from settings import *
from piece import *
from circle import *



class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = [[None for _ in range(8)] for _ in range(8)] 


        # Dashboard
        self.image_dashboard = pygame.image.load(join("img", "board.png")).convert_alpha()
        self.rect_dashboard = self.image_dashboard.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
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
                    for piece in self.group_sprites:
                        piece.delete_path()
                        if not self.selected_piece and piece.rect.collidepoint(event.pos):
                            self.selected_piece = True
                            piece.draw_path(self.image_dashboard)
                            print(piece.rect)
                        
                    self.selected_piece = False
                    
                        

            self.show_screen()
            self.draw_pieces()
            #print(self.board)

    def draw_bishops(self, centerx, top, bottom):
        """Call all bishops """
        self.board[0][2] = Bishop("black_bishop.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] * 1.5 ), 
                                    (top + SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.black_group))
        self.board[0][5] = Bishop("black_bishop.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] * 1.5), 
                                    (top + SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.black_group))

        Bishop("white_bishop.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] * 1.5), 
                                    (bottom - SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.white_group))
        Bishop("white_bishop.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] * 1.5), 
                                    (bottom - SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.white_group))

    def draw_kings_queens(self, centerx, top, bottom):
        King("black_king.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] / 2), 
                                (top + SQUARE_SIZE[1] / 2)), 
                                (self.group_sprites, self.black_group))

        Queen("black_queen.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] / 2), 
                                (top + SQUARE_SIZE[1] / 2)), 
                                (self.group_sprites, self.black_group))

        King("white_king.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] / 2), 
                                (bottom - SQUARE_SIZE[1] / 2)), 
                                (self.group_sprites, self.white_group))

        Queen("white_queen.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] / 2), 
                                (bottom - SQUARE_SIZE[1] / 2 )), 
                                (self.group_sprites, self.white_group))

    def draw_knights(self, centerx, top, bottom):
        Knight("black_knight.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] * 2.5), 
                                    (top + SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.black_group))
        Knight("black_knight.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] * 2.5), 
                                    (top + SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.black_group))

        Knight("white_knight.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] * 2.5), 
                                    (bottom - SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.white_group))
        Knight("white_knight.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] * 2.5), 
                                    (bottom - SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.white_group))

    def draw_rooks(self, centerx, top, bottom):
        Rook("black_rook.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] * 3.5), 
                                    (top + SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.black_group))
        Rook("black_rook.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] * 3.5), 
                                    (top + SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.black_group))

        Rook("white_rook.png", self.rect_dashboard, ((centerx - SQUARE_SIZE[0] * 3.5), 
                                    (bottom - SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.white_group))
        Rook("white_rook.png", self.rect_dashboard, ((centerx + SQUARE_SIZE[0] * 3.5), 
                                    (bottom - SQUARE_SIZE[1] / 2)), 
                                    (self.group_sprites, self.white_group))

    def draw_pawns(self, top, bottom, left):
        for i in range(8):
            Pawn("black_pawn.png", self.rect_dashboard, (((left + SQUARE_SIZE[0] * (i + 1)) - SQUARE_SIZE[0] / 2), 
                                    (top + SQUARE_SIZE[1] * 1.5)), 
                                    (self.group_sprites, self.black_group))
        for i in range(8):
            Pawn("white_pawn.png", self.rect_dashboard, (((left + SQUARE_SIZE[0]  * (i + 1)) - SQUARE_SIZE[0] / 2), 
                                    (bottom - SQUARE_SIZE[1] * 1.5)), 
                                    (self.group_sprites, self.white_group))


    def draw_pieces(self):
        """Draw all pieces"""
        centerx, top, bottom, left = self.rect_dashboard.center[0], self.rect_dashboard.top, self.rect_dashboard.bottom, self.rect_dashboard.left

        self.draw_bishops(centerx, top, bottom)
        self.draw_kings_queens(centerx, top, bottom)
        self.draw_knights(centerx, top, bottom)
        self.draw_rooks(centerx, top, bottom)
        self.draw_pawns(top, bottom, left)
 

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
