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

        # Black group
        self.black_group = pygame.sprite.Group()

        #print("Bottom", self.rect_dashboard.bottomleft)
        #print("Top", self.rect_dashboard.topleft)
        #print("Center", self.rect_dashboard.center)
        #print("4 squares", (self.rect_dashboard.center[1] - self.rect_dashboard.topleft[1]) / 4)
        #print("4 squares", (self.rect_dashboard.bottomleft[1] - self.rect_dashboard.center[1]) / 4)
        #print("left", self.rect_dashboard.bottomleft)
        #print("right", self.rect_dashboard.topright)
        #print("Center", self.rect_dashboard.center)
        #print("4 squares", (self.rect_dashboard.center[0] - self.rect_dashboard.left) / 4)
        #print("4 squares", (self.rect_dashboard.right - self.rect_dashboard.center[0]) / 4)

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

    def draw_pieces(self):
        Piece("black_bishop.png", (100, 100), (self.group_spites, self.black_group))

    def show_screen(self):
        dt = self.clock.tick() / 1000
        self.screen.fill("gray")

        # Draw the dashboard
        self.screen.blit(self.image_dashboard, self.rect_dashboard)

        # Draw all sprites
        self.group_spites.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
