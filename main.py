from settings import *
from piece import *


class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")

        # Dashboard
        self.image_dashboard = pygame.image.load(join("img", "board.png")).convert_alpha()
        self.rect_dashboard = self.image_dashboard.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
        # All group
        self.group_spites = pygame.sprite.Group()

        # Black  and white groups
        self.black_group = pygame.sprite.Group()
        self.white_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.show_screen()
            self.draw_pieces()

    def draw_bishops(self, centerx, top, bottom):
        """Call all bishops """
        Bishop("black_bishop.png", ((centerx - SQUARE_SIZE[0] * 6), 
                                    (top + SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.black_group))
        Bishop("black_bishop.png", ((centerx + SQUARE_SIZE[0] * 6), 
                                    (top + SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.black_group))

        Bishop("white_bishop.png", ((centerx - SQUARE_SIZE[0] * 6), 
                                    (bottom - SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.white_group))
        Bishop("white_bishop.png", ((centerx + SQUARE_SIZE[0] * 6), 
                                    (bottom - SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.white_group))

    def draw_kings_queens(self, centerx, top, bottom):
        King("black_king.png", ((centerx + SQUARE_SIZE[0] * 2), 
                                (top + SQUARE_SIZE[1] * 2)), 
                                (self.group_spites, self.black_group))

        Queen("black_queen.png", ((centerx - SQUARE_SIZE[0] * 2), 
                                (top + SQUARE_SIZE[1] * 2)), 
                                (self.group_spites, self.black_group))

        King("white_king.png", ((centerx + SQUARE_SIZE[0] * 2), 
                                (bottom - SQUARE_SIZE[1] * 2)), 
                                (self.group_spites, self.white_group))

        Queen("white_queen.png", ((centerx - SQUARE_SIZE[0] * 2), 
                                (bottom - SQUARE_SIZE[1] * 2)), 
                                (self.group_spites, self.white_group))

    def draw_knights(self, centerx, top, bottom):
        Knight("black_knight.png", ((centerx - SQUARE_SIZE[0] * 10), 
                                    (top + SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.black_group))
        Knight("black_knight.png", ((centerx + SQUARE_SIZE[0] * 10), 
                                    (top + SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.black_group))

        Knight("white_knight.png", ((centerx - SQUARE_SIZE[0] * 10), 
                                    (bottom - SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.white_group))
        Knight("white_knight.png", ((centerx + SQUARE_SIZE[0] * 10), 
                                    (bottom - SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.white_group))

    def draw_rooks(self, centerx, top, bottom):
        Rook("black_rook.png", ((centerx - SQUARE_SIZE[0] * 14), 
                                    (top + SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.black_group))
        Rook("black_rook.png", ((centerx + SQUARE_SIZE[0] * 14), 
                                    (top + SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.black_group))

        Rook("white_rook.png", ((centerx - SQUARE_SIZE[0] * 14), 
                                    (bottom - SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.white_group))
        Rook("white_rook.png", ((centerx + SQUARE_SIZE[0] * 14), 
                                    (bottom - SQUARE_SIZE[1] * 2)), 
                                    (self.group_spites, self.white_group))

    def draw_pawns(self, centerx, top, bottom, left):
        for i in range(1, 9):
            Pawn("black_pawn.png", (((left + SQUARE_SIZE[0] * 4 * i) - SQUARE_SIZE[0] * 2 ), 
                                    (top + SQUARE_SIZE[1] * 6)), 
                                    (self.group_spites, self.black_group))
        for i in range(1, 9):
            Pawn("white_pawn.png", (((left + SQUARE_SIZE[0] * 4 * i) - SQUARE_SIZE[0] * 2 ), 
                                    (bottom - SQUARE_SIZE[1] * 6)), 
                                    (self.group_spites, self.white_group))


    def draw_pieces(self):
        """Draw all pieces"""
        centerx, top, bottom, left = self.rect_dashboard.center[0], self.rect_dashboard.top, self.rect_dashboard.bottom, self.rect_dashboard.left

        self.draw_bishops(centerx, top, bottom)
        self.draw_kings_queens(centerx, top, bottom)
        self.draw_knights(centerx, top, bottom)
        self.draw_rooks(centerx, top, bottom)
        self.draw_pawns(centerx, top, bottom, left)
 

    def show_screen(self):
        dt = self.clock.tick() / 1000
        self.screen.fill("gray")

        # Draw the dashboard
        self.screen.blit(self.image_dashboard, self.rect_dashboard)

        # Draw all sprites
        self.group_spites.draw(self.screen)
        self.group_spites.update(dt)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
