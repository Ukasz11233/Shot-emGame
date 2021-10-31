import pygame
from Settings import *
from Functions import *
from random import randrange


# Enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, meteor_image):
        pygame.sprite.Sprite.__init__(self)
        self.speed_y = random.randrange(1, 5)
        self.speed_x = random.randrange(-3, 3)
        self.image_orig = meteor_image       # original image used in rotating meteor
        self.image_orig = pygame.transform.smoothscale(self.image_orig, (50 - self.speed_y*7, 50 - self.speed_y*7))  # transforming image to our scale
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        # using circle as collision model
        self.radius = (self.rect.width / 2) * 0.9

        # randomly spawning meteor
        self.rect.centerx = random.randrange(WIDTH - self.rect.width)
        self.rect.top = random.randrange(-100, -50)

        # damage:  slower and bigger meteors deal less damage; faster and smaller meteors deal more damage
        self.damage = 7 - (self.speed_y + 1)

        # variable used for rotating meteor
        self.rotation = 0
        self.rotation_speed = random.randrange(-10, 10)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):

        # checking condition of rotation frequency
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            center = self.rect.center
            self.last_update = now
            self.rotation = (self.rotation_speed + self.rotation) % 360  # this is angle on which we will rotate meteor
            self.image = pygame.transform.rotate(self.image_orig, self.rotation)   # rotating ORIGINAL IMAGE of meteor by some angle

            # placing meteor in the same place as before rotation
            self.rect = self.image.get_rect()
            self.rect.center = center


    def update(self):

        # checking if meteor have disappeared on our screen
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.rotate()



# Explosion sprite class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosion_animation, type, center):
        pygame.sprite.Sprite.__init__(self)
        # initializing image as one from our dictionary intialised in game class
        self.type = type
        self.image = explosion_animation[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # setting up frame of explosion animation
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 15


    def update(self, explosion_animation):

        # checking condition of explosion frequency
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1  # variable for changing explosion image

            # animation of explosion condition
            if self.frame >= len(explosion_animation[self.type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.type][self.frame] # changing explosion image
                self.rect = self.image.get_rect()
                self.rect.center = center
