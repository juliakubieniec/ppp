
import pygame
from random import randint

class BaseObject:
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path)
        self.x = x
        self.y = y

    def collision(self, obj):
        var_x = self.x > obj.x + obj.image.get_width() or self.x + self.image.get_width() < obj.x
        var_y = self.y > obj.y + obj.image.get_height() or self.y + self.image.get_height() < obj.y
        if var_x or var_y:
            return False
        else:
            return True

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_positoin(self):
        return (self.x, self.y)


class Asteroid(BaseObject):
    def __init__(self, x, y, speed):
        asteroid_type = randint(1,4)
        self.speed = speed
        self.points = asteroid_type * 10
        self.alive = True
        if asteroid_type == 1:
            path = 'images/asteroid1.png'
        elif asteroid_type == 2:
            path = 'images/asteroid2.png'
        elif asteroid_type == 3:
            path = 'images/asteroid3.png'
        else:
            path = 'images/asteroid4.png'
        BaseObject.__init__(self, path, x, y)


class Ship(BaseObject):
    def __init__(self, x, y):
        self.score = 0
        self.alive = True
        self.bullets = []
        BaseObject.__init__(self, 'images/ship.png', x, y)

    def shot(self):
        bullet = Bullet(0, 0)
        bullet.x = self.x + 0.5 * self.image.get_width() - 0.5 * bullet.image.get_width() + 1
        bullet.y = self.y - 0.2 * bullet.image.get_height()
        self.bullets.append(bullet)


class Bullet(BaseObject):
    def __init__(self, x, y):
        BaseObject.__init__(self, 'images/bullet.png', x, y)


class Star(BaseObject):
    def __init__(self, x, y, speed):
        self.speed = speed
        star_type = randint(1,3)
        if star_type == 1:
            path = 'images/star1.png'
        elif star_type == 2:
            path = 'images/star2.png'
        else:
            path = 'images/star3.png'
        BaseObject.__init__(self, path, x, y)
