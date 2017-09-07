# Source: https://github.com/pathunstrom/game-tutorial

from ppb import GameEngine, BaseScene
from pygame import image
from pygame.sprite import DirtySprite


class Player(DirtySprite):

    def __init__(self, scene):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.scene = scene


class Game(BaseScene):

    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)



# Main loop to keep the GUI running (60 times/sec)
def main():
    with GameEngine(Game, resolution=(400, 600)) as engine:
        engine.run()

if __name__ == "__main__":
    main()