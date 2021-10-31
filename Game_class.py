import pygame
from Settings import *
from Spaceship_class import *
from Enemy_class import *
from Functions import *
from os import path


# main game class
class Game:
    def __init__(self):

        # setting up display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shoot them all")

        # main loop variable condition
        self.running = True

        # initializing clock
        self.clock = pygame.time.Clock()

        # initializing sprites groups
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # initializing player
        self.player = Spaceship()

        # initialazing enemies frame
        self.enemy_frame = 60
        self.last_enemy = 0

        #initialzing actual score
        self.score = 0

        # list containing types of meteors
        self.enemies_types = [pygame.image.load(path.join(img_dir, 'meteorBig.png')).convert(), pygame.image.load(path.join(img_dir, 'meteorSmall.png')).convert()]
        self.explosion_animation = {}  #  dictionary containing graphic used in explosion animations
        self.explosion_animation['big'] = []   # bullet - meteor
        self.explosion_animation['small'] = []  # meteor - spaceship
        self.explosion_animation['player'] = []   # player.kill()

        #sounds
        pygame.mixer.init()
        self.shot_sound = pygame.mixer.Sound(path.join(sound_dir, 'shot.wav'))
        self.explosion_sound = pygame.mixer.Sound(path.join(sound_dir, 'explosion.wav'))

        # loops filling 'explosion_animation' dictionary with images from director: explosions
        for i in range(2):
            for j in range(10):
                filename = 'expl{}{}.png'.format(i, j)
                img = pygame.image.load(path.join(img_expl, filename)).convert()
                img.set_colorkey(BLACK)
                img_big = pygame.transform.scale(img, (60, 60))  # transforming size for meteor - bullet explosion
                self.explosion_animation['big'].append(img_big)
                img_small = pygame.transform.scale(img, (20, 20))  # transforming size for meter - player explosion
                self.explosion_animation['small'].append(img_small)
                img_player_expl = pygame.transform.scale(img, (250, 250))  # transofrming size for player.kill()
                self.explosion_animation['player'].append(img_player_expl)


    def run(self):
        # initializing background and player
        background = pygame.image.load(path.join(img_dir, 'back.png')).convert_alpha()
        background_rect = background.get_rect()
        self.sprites.add(self.player)

        # loading music
        pygame.mixer.music.load(path.join(sound_dir, 'music_for_game.wav'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

        # player explosion sprite
        player_explosion = Explosion(self.explosion_animation, 'player', self.player.rect.center)

        # main loop
        while self.running:
            self.clock.tick(FPS)
            self.add_events()
            self.update(player_explosion)
            self.draw(background, background_rect)
        pygame.quit()


    def draw(self, background, background_rect):
        self.screen.blit(background, background_rect)  # displaying background image on screen
        self.sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        draw_score(self.screen, str(self.score), 20, WIDTH / 2, 20)   # displaying current score on screen
        draw_lives(self.screen, self.player.lives, WIDTH , 10, self.player.lives_image)  # dislaying current lives counter

        # after all changes flip display
        pygame.display.flip()


    def add_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        # stop condition for clicking 'x' on the screen frame
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        # movement events
        if keys[pygame.K_LEFT]:
            if self.player.rect.left >= 5:
                self.player.rect.x -= 5
        elif keys[pygame.K_RIGHT]:
            if self.player.rect.right <= 355:
                self.player.rect.x += 5
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.player.last_shot > self.player.shot_delay:
                self.bullets.add(Bullet(self.player.rect.centerx), BulletShot(self.player.rect.centerx, self.player.rect.top))
                self.player.last_shot = now
                self.shot_sound.play()


    def update(self, player_explosion):

        # spawning meteor
        now = pygame.time.get_ticks()
        if now - self.last_enemy > self.enemy_frame:  #
            self.last_enemy = now
            self.enemies.add(Enemy(self.enemies_types[random.randrange(0, 2)]))

        # enemy - bullet collisions
        for hit in pygame.sprite.groupcollide(self.enemies, self.bullets, True, True):
            self.explosions.add(Explosion(self.explosion_animation, 'big', hit.rect.center))
            self.explosion_sound.play()
            self.score += hit.speed_y  # updating score

        # enemy - player collisions
        for hit in pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_circle):
            self.explosions.add(Explosion(self.explosion_animation, 'small',hit.rect.center))
            self.player.lives -= 1
            self.explosion_sound.play()

        # updating sprites groups
        self.sprites.update()
        self.explosions.update(self.explosion_animation)
        self.enemies.update()
        self.bullets.update()

        # checking if player is still alive
        if self.player.lives <= 0:
            if self.player.alive():  # if player have 0 lives - kill him
                player_explosion.rect.center = self.player.rect.center
                self.explosions.add(player_explosion)
                self.player.kill()
            else: # if player is already dead, run only explosion sprite
                if not player_explosion.alive():
                    self.running = False