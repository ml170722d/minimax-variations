import traceback
import pygame

from game import Game


def main():
    try:
        pygame.init()
        g = Game()
        g.run()
    except KeyboardInterrupt:
        pass
    except (Exception,):
        traceback.print_exc()
        input()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
