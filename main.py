# Source: https://github.com/pathunstrom/game-tutorial
import csv
from itertools import count
from os import path

from ppb import GameEngine, BaseScene
from pygame import image, mouse, Rect
from pygame.sprite import DirtySprite, groupcollide



ROOT_DIR = path.dirname(__file__)


class Spawner(object):
    def __init__(self, scene, generator, enemy_class):
        self.scene = scene
        self.enemy_class = enemy_class
        self.generator = generator
        self.time = 0
        self.next_time = None
        self.next_position = None
        self.running = True
        self.prime()

    def spawn(self, time_delta):
        self.time += time_delta
        while self.running and self.time >= self.next_time:
            self.enemy_class(self.scene, self.next_position)
            self.prime()

    def prime(self):
        try:
            self.next_time, self.next_position = next(self.generator)
        except StopIteration:
            self.running = False


class BaseGameObject(DirtySprite):
    group = None
    image_path = None
    image = None

    def __init__(self, scene, position=(0, 0)):
        cls = self.__class__
        cls.group = cls.__name__
        super().__init__(scene.groups[cls.group], scene.groups["render"])
        self.scene = scene
        cls.image = image.load(path.join(ROOT_DIR, cls.image_path))
        self.rect = cls.image.get_rect()
        self.rect.center = position
        # self.rect.center = (720, 800)
        self.last_position = position

    def update(self, time_delta):
        self.simulate(time_delta)
        if self.rect.center != self.last_position:
            self.dirty = True
            self.last_position = self.rect.center
    # def simulate(self, time_delta):
    #     pass


class Player(BaseGameObject):
    image_path = "player.png"

    def __init__(self, scene):
        super().__init__(scene)
        # self.rect.center = (720, 0)
        self.laser_limiter = 0.5
        self.laser_delay = 0

    def simulate(self, time_delta):
        mouse_x, mouse_y = mouse.get_pos()
        diff_x = max(min(mouse_x - self.rect.centerx, 10), -10)
        diff_y = max(min(mouse_y - self.rect.centery, 10), -10)
        self.rect.centerx += diff_x
        self.rect.centery += diff_y

        pressed = mouse.get_pressed()
        if pressed[0] and (self.laser_delay >= self.laser_limiter):
            Laser(self.scene, self.rect.midtop)
            self.laser_delay = 0
        self.laser_delay += time_delta


class Laser(BaseGameObject):
    image_path = "laser.png"

    def simulate(self, time_delta):
        self.rect.centery += -10


class Enemy(BaseGameObject):
    image_path = "enemy.png"

    def __init__(self, scene, x_position):
        super().__init__(scene, (x_position, 50))

    def simulate(self, time_delta):
        self.rect.centery += 3


class Game(BaseScene):

    def __init__(self, engine, background_color=(0, 0, 0), **kwargs):
        super().__init__(engine=engine,
                         background_color=background_color,
                         **kwargs)
        engine.display.fill(background_color)
        Player(self)
        Laser(self, (0, 0)).kill()
        self.spawner = Spawner(self, file_spawner('spawn.csv'), Enemy)
        # Enemy(self, 200)

    def simulate(self, time_delta):
        super().simulate(time_delta)
        self.spawner.spawn(time_delta)
        player = self.groups[Player.group]
        lasers = self.groups[Laser.group]
        enemies = self.groups[Enemy.group]
        groupcollide(player, enemies, True, True)
        groupcollide(enemies, lasers, True, True)


# Generator that outputs 2-tuple timestamp in secs
def simple_infinite_spawn(time_step, x_val):
    for value in count(1):
        time = time_step * value
        yield time, x_val


# Create new generator
def file_spawner(file_name):
    with open(path.join(path.dirname(__file__), file_name), "r") as spawn_file:
        spawn_reader = csv.reader(spawn_file)
        for row in spawn_reader:
            yield float(row[0]), int(row[1])


# Main loop to keep the GUI running (60 times/sec)
def main():
    with GameEngine(Game, resolution=(1440, 900)) as engine:
        engine.run()

if __name__ == "__main__":
    main()

