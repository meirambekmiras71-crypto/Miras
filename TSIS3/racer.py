import pygame
import random
import time
from pygame.locals import *

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 200, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 200, 0)
ORANGE = (255, 140, 0)
PURPLE = (150, 0, 200)
GRAY   = (180, 180, 180)

CAR_COLORS = {
    "blue":   BLUE,
    "red":    RED,
    "green":  GREEN,
    "yellow": YELLOW,
}

DIFFICULTY_SETTINGS = {
    "easy":   {"enemy_count": 1, "obstacle_count": 1, "speed": 4},
    "normal": {"enemy_count": 2, "obstacle_count": 2, "speed": 5},
    "hard":   {"enemy_count": 3, "obstacle_count": 3, "speed": 7},
}

font_small  = None
font_medium = None


def init_fonts():
    global font_small, font_medium
    font_small  = pygame.font.SysFont("Verdana", 18)
    font_medium = pygame.font.SysFont("Verdana", 24)


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        car_color = CAR_COLORS.get(color_name, BLUE)
        pygame.draw.rect(self.image, car_color, (5, 10, 30, 50), border_radius=6)
        pygame.draw.rect(self.image, BLACK, (7, 15, 26, 20), border_radius=4)
        pygame.draw.rect(self.image, BLACK, (5, 10, 8, 14), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (27, 10, 8, 14), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (5, 52, 8, 14), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (27, 52, 8, 14), border_radius=3)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)
        self.shield = False
        self.nitro  = False
        self.nitro_end   = 0
        self.shield_active = False

    def move(self, speed_boost=0):
        keys = pygame.key.get_pressed()
        spd = 7 + speed_boost if self.nitro else 5 + speed_boost
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-spd, 0)
        if self.rect.right < SCREEN_WIDTH and keys[K_RIGHT]:
            self.rect.move_ip(spd, 0)

    def update_powerups(self):
        now = pygame.time.get_ticks()
        if self.nitro and now > self.nitro_end:
            self.nitro = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (5, 10, 30, 50), border_radius=6)
        pygame.draw.rect(self.image, BLACK, (7, 15, 26, 20), border_radius=4)
        pygame.draw.rect(self.image, BLACK, (5, 10, 8, 14), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (27, 10, 8, 14), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (5, 52, 8, 14), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (27, 52, 8, 14), border_radius=3)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -random.randint(0, 300))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -random.randint(50, 300))
            self.speed = max(self.speed, self.speed + random.uniform(0, 0.3))


class Coin(pygame.sprite.Sprite):
    WEIGHTS = [(1, 60), (3, 30), (5, 10)]

    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        self.value = random.choices([v for v, _ in self.WEIGHTS], [w for _, w in self.WEIGHTS])[0]
        color = YELLOW if self.value == 1 else ORANGE if self.value == 3 else WHITE
        pygame.draw.circle(self.image, color, (12, 12), 12)
        lbl = pygame.font.SysFont("Verdana", 12).render(str(self.value), True, BLACK)
        self.image.blit(lbl, (12 - lbl.get_width() // 2, 12 - lbl.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), -random.randint(0, 400))
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), -random.randint(50, 400))


class Obstacle(pygame.sprite.Sprite):
    TYPES = [
        {"label": "OIL",  "color": (30,  30,  30),  "effect": "slow"},
        {"label": "BUMP", "color": (120, 80,  40),   "effect": "slow"},
        {"label": "ROCK", "color": (100, 100, 100),  "effect": "stop"},
    ]

    def __init__(self, speed):
        super().__init__()
        t = random.choice(self.TYPES)
        self.effect = t["effect"]
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, t["color"], (0, 0, 50, 30))
        lbl = pygame.font.SysFont("Verdana", 11).render(t["label"], True, WHITE)
        self.image.blit(lbl, (25 - lbl.get_width() // 2, 8))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -random.randint(0, 300))
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -random.randint(50, 300))


class PowerUp(pygame.sprite.Sprite):
    TYPES = [
        {"kind": "nitro",  "color": ORANGE, "label": "N"},
        {"kind": "shield", "color": BLUE,   "label": "S"},
        {"kind": "repair", "color": GREEN,  "label": "R"},
    ]

    def __init__(self, speed):
        super().__init__()
        t = random.choice(self.TYPES)
        self.kind = t["kind"]
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.image, t["color"], (0, 0, 32, 32), border_radius=8)
        lbl = pygame.font.SysFont("Verdana", 18, bold=True).render(t["label"], True, WHITE)
        self.image.blit(lbl, (16 - lbl.get_width() // 2, 16 - lbl.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), -random.randint(0, 400))
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime


def draw_road(surface, offset):
    surface.fill((60, 60, 60))
    for lane_x in [100, 200, 300]:
        for y in range(-40 + offset % 80, SCREEN_HEIGHT, 80):
            pygame.draw.rect(surface, YELLOW, (lane_x - 3, y, 6, 40))
    pygame.draw.rect(surface, WHITE, (20, 0, 6, SCREEN_HEIGHT))
    pygame.draw.rect(surface, WHITE, (374, 0, 6, SCREEN_HEIGHT))


def draw_hud(surface, score, distance, coins, player, active_powerup, powerup_timer):
    pygame.draw.rect(surface, (0, 0, 0, 160), (0, 0, SCREEN_WIDTH, 60))
    score_s   = font_small.render(f"Score: {score}",      True, WHITE)
    dist_s    = font_small.render(f"Dist: {distance}m",   True, WHITE)
    coins_s   = font_small.render(f"Coins: {coins}",      True, YELLOW)
    surface.blit(score_s, (5,  5))
    surface.blit(dist_s,  (5,  25))
    surface.blit(coins_s, (5,  45))

    if player.shield_active:
        sh = font_small.render("SHIELD", True, BLUE)
        surface.blit(sh, (SCREEN_WIDTH - 80, 5))

    if active_powerup and powerup_timer > 0:
        t = font_small.render(f"{active_powerup.upper()} {powerup_timer:.1f}s", True, ORANGE)
        surface.blit(t, (SCREEN_WIDTH - 120, 25))


def run_game(surface, settings, username):
    init_fonts()
    clock = pygame.time.Clock()

    diff = DIFFICULTY_SETTINGS[settings.get("difficulty", "normal")]
    base_speed = diff["speed"]
    speed = base_speed

    player = Player(settings.get("car_color", "blue"))

    enemies   = pygame.sprite.Group()
    coins     = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups  = pygame.sprite.Group()

    for _ in range(diff["enemy_count"]):
        enemies.add(Enemy(speed))
    for _ in range(3):
        coins.add(Coin(speed))
    for _ in range(diff["obstacle_count"]):
        obstacles.add(Obstacle(speed))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)
    all_sprites.add(coins)
    all_sprites.add(obstacles)

    score        = 0
    coin_score   = 0
    distance     = 0
    road_offset  = 0
    slow_timer   = 0
    active_powerup    = None
    powerup_end_time  = 0

    SPAWN_POWERUP = pygame.USEREVENT + 1
    INC_SPEED     = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_POWERUP, 7000)
    pygame.time.set_timer(INC_SPEED,     3000)

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit", score, distance, coin_score
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                return "menu", score, distance, coin_score
            if event.type == SPAWN_POWERUP:
                if len(powerups) == 0:
                    pu = PowerUp(speed)
                    powerups.add(pu)
                    all_sprites.add(pu)
            if event.type == INC_SPEED:
                speed += 0.3
                for e in enemies:
                    e.speed = speed
                for c in coins:
                    c.speed = speed
                for o in obstacles:
                    o.speed = speed

        now = pygame.time.get_ticks()

        player.update_powerups()
        if active_powerup and now > powerup_end_time:
            active_powerup = None

        speed_boost = 3 if player.nitro else 0
        player.move(speed_boost)

        for e in enemies:
            e.move()
        for c in coins:
            c.move()
        for o in obstacles:
            o.move()
        for pu in list(powerups):
            pu.move()
            if pu.is_expired():
                pu.kill()
                all_sprites.remove(pu)

        road_offset = (road_offset + int(speed)) % 80
        distance    = int(distance + speed * 0.05)
        score       = coin_score * 10 + distance

        collected = pygame.sprite.spritecollide(player, coins, False)
        for c in collected:
            coin_score += c.value
            c.rect.center = (random.randint(20, SCREEN_WIDTH - 20), -random.randint(50, 400))
            c.value = random.choices([v for v, _ in Coin.WEIGHTS], [w for _, w in Coin.WEIGHTS])[0]

        hit_obstacles = pygame.sprite.spritecollide(player, obstacles, False)
        for o in hit_obstacles:
            if o.effect == "slow":
                slow_timer = now + 2000
            o.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -random.randint(50, 300))

        if slow_timer > now:
            speed = max(base_speed - 2, 2)
        else:
            speed = base_speed + distance * 0.001

        collected_pu = pygame.sprite.spritecollide(player, powerups, True)
        for pu in collected_pu:
            all_sprites.remove(pu)
            if pu.kind == "nitro":
                player.nitro = True
                player.nitro_end = now + 4000
                active_powerup   = "nitro"
                powerup_end_time = now + 4000
            elif pu.kind == "shield":
                player.shield_active = True
                active_powerup   = "shield"
                powerup_end_time = now + 999999
            elif pu.kind == "repair":
                slow_timer = 0
                active_powerup = None

        hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
        if hit_enemies:
            if player.shield_active:
                player.shield_active = False
                active_powerup = None
                for e in hit_enemies:
                    e.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -random.randint(50, 300))
            else:
                if settings.get("sound", True):
                    try:
                        pygame.mixer.Sound("crash.wav").play()
                    except Exception:
                        pass
                time.sleep(0.5)
                return "gameover", score, distance, coin_score

        powerup_timer = max(0, (powerup_end_time - now) / 1000) if active_powerup == "nitro" else 0

        draw_road(surface, road_offset)
        for sprite in all_sprites:
            surface.blit(sprite.image, sprite.rect)
        draw_hud(surface, score, distance, coin_score, player, active_powerup, powerup_timer)

        pygame.display.flip()

    return "menu", score, distance, coin_score