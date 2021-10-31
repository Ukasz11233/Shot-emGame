import pygame
from Settings import *
from Game_class import *

# Spaceship sprite class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # initializing image
        self.image = pygame.image.load(path.join(img_dir, 'player.png')).convert()
        self.image = pygame.transform.smoothscale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)

        # using circle as collision model
        self.radius = 20
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 480

        # setting up number of lives for player
        self.lives = 5

        # live icon (appears in the top right corner on the screen)
        self.lives_image = self.image.copy()
        self.lives_image = pygame.transform.smoothscale(self.lives_image, (25, 15))

        # variable used for changing spaceship image when its get damaged
        self.transformed = False

        # shot frequency
        self.shot_delay = 250
        self.last_shot = pygame.time.get_ticks()


    def update(self):

        # changing spaceship image when it gets damaged
        if self.lives < 3:
            self.image = pygame.image.load(path.join(img_dir, 'playerDamaged.png')).convert()
            self.image = pygame.transform.smoothscale(self.image, (50, 50))
            self.image.set_colorkey(BLACK)




# Bullet sprite class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        # initializing image
        self.image = pygame.image.load(path.join(img_dir, 'laserRed.png')).convert()
        self.image = pygame.transform.smoothscale(self.image, (5, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 40
        self.rect.centerx = pos


    def update(self):

        # if bullet disappears from screen it gets killed
        if self.rect.bottom < 0:
            self.kill()

        # setting up speed of bullet
        self.rect.y -= 6



# Bulletshot sprite class
class BulletShot(pygame.sprite.Sprite):
    def __init__(self, center_x, top):
        pygame.sprite.Sprite.__init__(self)

        # initializing image of explosion when firing
        self.image = pygame.image.load(path.join(img_dir, 'laserRedShot.png')).convert()
        self.image = pygame.transform.smoothscale(self.image, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = top
        self.rect.centerx = center_x
        self.frequency = 25
        self.fired = pygame.time.get_ticks()


    def update(self):

        # checking condition of bullet shot explosion frequency
        now = pygame.time.get_ticks()
        if now - self.fired > self.frequency:
            self.kill()
