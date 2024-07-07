from settings import *



class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")

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

    def show_screen(self):
        dt = self.clock.tick() / 1000
        self.screen.fill("blue")
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
