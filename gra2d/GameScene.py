
from abc import abstractmethod
from GameObject import *

STEP = 5
STAR_AMOUNT = 300
ASTEROID_AMOUNT = 20

class BaseScene:
    def __init__(self):
        self.next = self

    @abstractmethod
    def process_input(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    def switch_scene(self, scene):
        self.next = scene

    def terminate(self):
        self.switch_scene(None)

    def text_to_screen(self, screen, text, x, y, size = 50,
                       color = (000, 000, 80), font_type = 'comicsansms'):
            text = str(text)
            font = pygame.font.SysFont(font_type, size)
            text = font.render(text, True, color)
            screen.blit(text, (x, y))

    def run_game(self, width, height, fps, scene):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()

        active_scene = scene

        while active_scene != None:
            pressed_key = pygame.key.get_pressed()
            filtered_events = []
            for event in pygame.event.get():
                quit_event = False
                if event.type == pygame.QUIT:
                    quit_event = True
                elif event.type == pygame.KEYDOWN:
                    alt_pressed = pressed_key[pygame.K_LALT] or pressed_key[pygame.K_RALT]
                    if event.key == pygame.K_ESCAPE:
                        quit_event = True
                    elif event.key == pygame.K_F4 and alt_pressed:
                        quit_event = True;

                if quit_event:
                    active_scene.terminate()
                else:
                    filtered_events.append(event)

            active_scene.process_input(filtered_events)
            active_scene.update()
            active_scene.render(screen)

            active_scene = active_scene.next

            pygame.display.flip()
            clock.tick(fps)


class TitleScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_p):
                self.switch_scene(GameScene())

    def update(self):
        pass

    def render(self, screen):
        screen.fill(pygame.Color('gray'))
        self.text_to_screen(screen, 'Asteroids', 200, 100, size=80)
        self.text_to_screen(screen, '[p]lay', 330, 250)


class GameScene(BaseScene):
    def __init__(self):
        self.ship = Ship(350,530)
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.pressed_key = []
        self.asteroids = []
        self.stars = []
        self.create_asteroids()
        self.create_star()
        self.high_score = self.load_high_store()
        BaseScene.__init__(self)

    def create_asteroids(self):
        for i in range(0, ASTEROID_AMOUNT):
            self.asteroids.append(Asteroid(randint(20, self.screen_width - 20), randint(0, 100), randint(2,4)))

    def create_star(self):
        for i in range(0, STAR_AMOUNT):
            self.stars.append(Star(randint(1,self.screen_width), randint(1,self.screen_height), randint(5,8)))

    def load_high_store(self):
        try:
            f = open("hs.txt","rb")
            hs = int(f.read())
            f.close()
            return hs
        except:
            return 0

    def write_high_store(self):
        f = open("hs.txt","wb")
        f.write(str(self.high_score).encode())
        f.close()

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.pressed_key.append(event.key)
            if event.type == pygame.KEYUP and len(self.pressed_key) > 0:
                self.pressed_key.pop(len(self.pressed_key) - 1)
        for key in self.pressed_key:
            if key == pygame.K_LEFT:
                if self.ship.x - STEP >= 0:
                    self.ship.x -= STEP
            if key == pygame.K_RIGHT:
                if self.ship.x + self.ship.image.get_width() + STEP <= self.screen_width:
                    self.ship.x += STEP
            if key == pygame.K_SPACE:
                self.ship.shot()

    def update(self):
        if self.ship.alive:
            self.check_collision()
            self.update_bullet()
            self.update_stars()
            self.update_asteroids()
            if self.high_score == 0:
                self.high_score = self.ship.score
        else:
            del self.ship.bullets[:]
            del self.asteroids[:]
            del self.stars[:]
            if self.ship.score > self.high_score:
                self.high_score = self.ship.score
            self.write_high_store()
            self.switch_scene(OverScene())

    def check_collision(self):
        for asteroid in self.asteroids:
            if asteroid.collision(self.ship):
                self.ship.alive = False
                break
        for asteroid in self.asteroids:
            for bullet in self.ship.bullets:
                if asteroid.collision(bullet):
                    self.ship.score += asteroid.points
                    asteroid.alive = False
                    self.ship.bullets.remove(bullet)

    def update_bullet(self):
        for bullet in self.ship.bullets:
            if bullet.y - STEP >= 0:
                bullet.y -= STEP
            else:
                self.ship.bullets.remove(bullet)

    def update_stars(self):
        for star in self.stars:
            star.y += star.speed
            if star.y > self.screen_height:
                star.y = 0

    def update_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.y += asteroid.speed
            if not asteroid.alive:
                asteroid.y = -10
                asteroid.alive = True
            elif asteroid.y > self.screen_height:
                asteroid.y = -10

    def render(self, screen):
        screen.fill(pygame.Color('navyblue'))
        self.text_to_screen(screen, 'Score: {0}'.format(self.ship.score), 5, 5, size=15, color=(000,255,000))
        self.text_to_screen(screen, 'High score: {0}'.format(self.high_score), 5, 25, size=15, color=(000,255,000))
        screen.blit(self.ship.image, self.ship.get_positoin())
        for star in self.stars:
            screen.blit(star.image, star.get_positoin())
        for asteroid in self.asteroids:
            screen.blit(asteroid.image, asteroid.get_positoin())
        for bullet in self.ship.bullets:
            screen.blit(bullet.image, bullet.get_positoin())


class OverScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.switch_scene(GameScene())
                elif event.key == pygame.K_n:
                    self.terminate()

    def update(self):
        pass

    def render(self, screen):
        screen.fill(pygame.Color('gray'))
        self.text_to_screen(screen, 'Jeszcze raz?', 150, 100, size=80)
        self.text_to_screen(screen, '[t]ak / [n]ie', 250, 250)
