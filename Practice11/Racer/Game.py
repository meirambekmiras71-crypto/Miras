import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
ENEMY_SPEED = 5
SPEED_INCREASE_THRESHOLD = 5

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize enemy sprite and position it at the top
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE, ENEMY_SPEED
        # Move enemy downward using the current enemy speed
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    # Coin weights: 1 = common, 3 = rare, 5 = very rare
    WEIGHTS = [
        (1, 60),
        (3, 30),
        (5, 10),
    ]

    def __init__(self):
        # Initialize coin with a random weight based on probability
        super().__init__()
        original_image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.value = self._random_value()

    def _random_value(self):
        # Select coin value based on weighted probability
        values = [v for v, _ in self.WEIGHTS]
        weights = [w for _, w in self.WEIGHTS]
        return random.choices(values, weights=weights, k=1)[0]

    def move(self):
        # Move coin downward; reset if it leaves the screen
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        # Reposition coin to the top with a new random weight
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.value = self._random_value()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize player sprite and position it near the bottom
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        # Move player left or right based on keyboard input
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            # Increase overall speed every second
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))

    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    speed_text = font_small.render("Enemy Speed: " + str(round(ENEMY_SPEED, 1)), True, BLACK)

    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 110, 10))
    DISPLAYSURF.blit(speed_text, (10, 35))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check if player collects a coin
    if pygame.sprite.spritecollide(P1, coins, False):
        COIN_SCORE += C1.value
        C1.reset()

        # Increase enemy speed every SPEED_INCREASE_THRESHOLD coins
        if COIN_SCORE % SPEED_INCREASE_THRESHOLD == 0:
            ENEMY_SPEED += 1

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)