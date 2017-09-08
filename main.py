# Source: https://github.com/pathunstrom/game-tutorial

from os import path

from ppb import GameEngine, BaseScene
from pygame import image, mouse
from pygame.sprite import DirtySprite, groupcollide


class Player(DirtySprite):

    def __init__(self, scene):
        super().__init__(scene.groups["player"])
        self.image = image.load(path.join(path.dirname(__file__),
                                          "player.png"))
        self.rect = self.image.get_rect()
        self.scene = scene
        self.laser_limiter = 0.25
        self.laser_delay = 0

    def simulate(self, time_delta):
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 5), -5)
        diff_y = max(min(mouse_y - self.rect.centery, 5), -5)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y

        pressed = mouse.get_pressed()
        if pressed[0] and (self.laser_delay >= self.laser_limiter):
            Laser(self.scene, self.rect.midtop)
            self.laser_delay = 0
        self.laser_delay += time_delta


class Laser(DirtySprite):

    def __init__(self, scene, position):
        super().__init__(scene.groups["lasers"])
        b_image = image.load(path.join(path.dirname(__file__), "laser.png"))
        self.image = b_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = position
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += -10
        self.dirty = True


class Game(BaseScene):

    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        engine.display.fill(background_color)
        Player(self)
        Laser(self, (300, 400)).kill()
        Enemy(self, 200)

    def simulate(self, time_delta):
        super().simulate(time_delta)
        player = self.groups["player"]
        lasers = self.groups["lasers"]
        enemies = self.groups["enemy"]
        groupcollide(player, enemies, True, True)
        groupcollide(enemies, lasers, True, True)


class Enemy(DirtySprite):

    def __init__(self, scene, x_position):
        super().__init__(scene.groups["enemy"])
        p_image = image.load(path.join(path.dirname(__file__), "enemy.png"))
        self.image = p_image
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.centerx = x_position
        self.scene = scene

    def update(self, time_delta):
        self.rect.centery += 3
        self.dirty = True


# Main loop to keep the GUI running (60 times/sec)
def main():
    with GameEngine(Game, resolution=(500, 750)) as engine:
        engine.run()

if __name__ == "__main__":
    main()