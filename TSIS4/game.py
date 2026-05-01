import pygame
import random
from config import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self, color):
        self.body  = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx    = 1
        self.dy    = 0
        self.color = color
        self.shield = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_collision_with_walls_and_self(self, obstacles):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            if self.shield:
                self.shield = False
                head.x = max(0, min(WIDTH // CELL - 1, head.x))
                head.y = max(0, min(HEIGHT // CELL - 1, head.y))
                return False
            return True
        for i in range(1, len(self.body)):
            if head.x == self.body[i].x and head.y == self.body[i].y:
                if self.shield:
                    self.shield = False
                    return False
                return True
        for ob in obstacles:
            if head.x == ob.x and head.y == ob.y:
                return True
        return False

    def grow(self):
        self.body.append(Point(self.body[-1].x, self.body[-1].y))

    def shorten(self, n=2):
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()

    def draw(self, surface, show_grid):
        head = self.body[0]
        pygame.draw.rect(surface, RED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for seg in self.body[1:]:
            pygame.draw.rect(surface, self.color, (seg.x * CELL, seg.y * CELL, CELL, CELL))


class Food:
    TYPES = [
        (1, GREEN,    None),
        (3, BLUE,     7),
        (5, WHITE,    4),
    ]

    def __init__(self, snake_body, all_food, obstacles):
        weights     = [60, 30, 10]
        chosen      = random.choices(self.TYPES, weights=weights, k=1)[0]
        self.value  = chosen[0]
        self.color  = chosen[1]
        self.lifetime   = chosen[2]
        self.spawn_time = pygame.time.get_ticks()
        self.pos        = Point(0, 0)
        self.is_poison  = False
        self.generate_random_pos(snake_body, all_food, obstacles)

    def is_expired(self):
        if self.lifetime is None:
            return False
        return (pygame.time.get_ticks() - self.spawn_time) / 1000 >= self.lifetime

    def time_left(self):
        if self.lifetime is None:
            return None
        return max(0, self.lifetime - (pygame.time.get_ticks() - self.spawn_time) / 1000)

    def generate_random_pos(self, snake_body, all_food, obstacles):
        blocked = {(s.x, s.y) for s in snake_body}
        blocked |= {(f.pos.x, f.pos.y) for f in all_food}
        blocked |= {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, WIDTH  // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if (x, y) not in blocked:
                self.pos.x = x
                self.pos.y = y
                break

    def draw(self, surface, font_small):
        pygame.draw.rect(surface, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        lbl = font_small.render(str(self.value), True, BLACK)
        surface.blit(lbl, (self.pos.x * CELL + 6, self.pos.y * CELL + 6))
        if self.lifetime is not None:
            t = font_small.render(f"{self.time_left():.1f}", True, RED)
            surface.blit(t, (self.pos.x * CELL, self.pos.y * CELL - 16))


class PoisonFood:
    def __init__(self, snake_body, all_food, obstacles):
        self.color      = DARK_RED
        self.pos        = Point(0, 0)
        self.is_poison  = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime   = 10
        self.generate_random_pos(snake_body, all_food, obstacles)

    def is_expired(self):
        return (pygame.time.get_ticks() - self.spawn_time) / 1000 >= self.lifetime

    def time_left(self):
        return max(0, self.lifetime - (pygame.time.get_ticks() - self.spawn_time) / 1000)

    def generate_random_pos(self, snake_body, all_food, obstacles):
        blocked = {(s.x, s.y) for s in snake_body}
        blocked |= {(f.pos.x, f.pos.y) for f in all_food}
        blocked |= {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, WIDTH  // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if (x, y) not in blocked:
                self.pos.x = x
                self.pos.y = y
                break

    def draw(self, surface, font_small):
        pygame.draw.rect(surface, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        lbl = font_small.render("P", True, WHITE)
        surface.blit(lbl, (self.pos.x * CELL + 6, self.pos.y * CELL + 6))
        t = font_small.render(f"{self.time_left():.1f}", True, ORANGE)
        surface.blit(t, (self.pos.x * CELL, self.pos.y * CELL - 16))


class PowerUp:
    TYPES = [
        {"kind": "speed",  "color": ORANGE, "label": "F"},
        {"kind": "slow",   "color": PURPLE, "label": "S"},
        {"kind": "shield", "color": BLUE,   "label": "SH"},
    ]

    def __init__(self, snake_body, all_food, obstacles):
        t           = random.choice(self.TYPES)
        self.kind   = t["kind"]
        self.color  = t["color"]
        self.label  = t["label"]
        self.pos        = Point(0, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime   = 8
        self.generate_random_pos(snake_body, all_food, obstacles)

    def is_expired(self):
        return (pygame.time.get_ticks() - self.spawn_time) / 1000 >= self.lifetime

    def time_left(self):
        return max(0, self.lifetime - (pygame.time.get_ticks() - self.spawn_time) / 1000)

    def generate_random_pos(self, snake_body, all_food, obstacles):
        blocked = {(s.x, s.y) for s in snake_body}
        blocked |= {(f.pos.x, f.pos.y) for f in all_food}
        blocked |= {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, WIDTH  // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if (x, y) not in blocked:
                self.pos.x = x
                self.pos.y = y
                break

    def draw(self, surface, font_small):
        pygame.draw.rect(surface, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        lbl = font_small.render(self.label, True, WHITE)
        surface.blit(lbl, (self.pos.x * CELL + 2, self.pos.y * CELL + 6))
        t = font_small.render(f"{self.time_left():.1f}", True, WHITE)
        surface.blit(t, (self.pos.x * CELL, self.pos.y * CELL - 16))


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, DGRAY, (self.x * CELL, self.y * CELL, CELL, CELL))
        pygame.draw.rect(surface, WHITE, (self.x * CELL, self.y * CELL, CELL, CELL), 1)


def generate_obstacles(level, snake_body):
    count   = (level - 2) * 2
    blocked = {(s.x, s.y) for s in snake_body}
    head    = snake_body[0]
    safe    = {(head.x + dx, head.y + dy) for dx in range(-2, 3) for dy in range(-2, 3)}
    obstacles = []
    attempts  = 0
    while len(obstacles) < count and attempts < 500:
        x = random.randint(0, WIDTH  // CELL - 1)
        y = random.randint(0, HEIGHT // CELL - 1)
        if (x, y) not in blocked and (x, y) not in safe:
            blocked.add((x, y))
            obstacles.append(Obstacle(x, y))
        attempts += 1
    return obstacles


def draw_grid(surface):
    for i in range(WIDTH  // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(surface, GRAY, (i * CELL, j * CELL, CELL, CELL), 1)


def run_game(surface, settings, player_id, personal_best):
    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 22)

    snake_color = tuple(settings.get("snake_color", list(YELLOW)))
    show_grid   = settings.get("grid", True)

    snake     = Snake(snake_color)
    obstacles = []
    food_list = [Food(snake.body, [], obstacles)]
    poison    = None
    powerup   = None

    score           = 0
    level           = 1
    fps             = FPS
    foods_to_level  = 3
    food_count      = 0

    active_powerup     = None
    powerup_end_time   = 0

    SPAWN_BONUS  = pygame.USEREVENT + 1
    SPAWN_POISON = pygame.USEREVENT + 2
    SPAWN_PU     = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_BONUS,  5000)
    pygame.time.set_timer(SPAWN_POISON, 8000)
    pygame.time.set_timer(SPAWN_PU,     10000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score, level
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1;  snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1; snake.dy = 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0;  snake.dy = 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0;  snake.dy = -1
            if event.type == SPAWN_BONUS and len(food_list) < 3:
                food_list.append(Food(snake.body, food_list, obstacles))
            if event.type == SPAWN_POISON and poison is None:
                poison = PoisonFood(snake.body, food_list, obstacles)
            if event.type == SPAWN_PU and powerup is None:
                powerup = PowerUp(snake.body, food_list, obstacles)

        now = pygame.time.get_ticks()

        if active_powerup and now > powerup_end_time:
            if active_powerup == "speed":
                fps = FPS + (level - 1) * 2
            elif active_powerup == "slow":
                fps = FPS + (level - 1) * 2
            active_powerup = None

        food_list = [f for f in food_list if not f.is_expired()]
        if not food_list:
            food_list.append(Food(snake.body, [], obstacles))

        if poison and poison.is_expired():
            poison = None
        if powerup and powerup.is_expired():
            powerup = None

        snake.move()

        if snake.check_collision_with_walls_and_self(obstacles):
            return score, level

        head = snake.body[0]

        for f in list(food_list):
            if head.x == f.pos.x and head.y == f.pos.y:
                score += f.value
                food_count += 1
                snake.grow()
                food_list.remove(f)
                food_list.append(Food(snake.body, food_list, obstacles))
                if food_count % foods_to_level == 0:
                    level += 1
                    fps += 2
                    if level >= 3:
                        obstacles = generate_obstacles(level, snake.body)
                break

        if poison and head.x == poison.pos.x and head.y == poison.pos.y:
            snake.shorten(2)
            poison = None
            if len(snake.body) <= 1:
                return score, level

        if powerup and head.x == powerup.pos.x and head.y == powerup.pos.y:
            if powerup.kind == "speed":
                fps += 3
                active_powerup   = "speed"
                powerup_end_time = now + 5000
            elif powerup.kind == "slow":
                fps = max(2, fps - 3)
                active_powerup   = "slow"
                powerup_end_time = now + 5000
            elif powerup.kind == "shield":
                snake.shield     = True
                active_powerup   = "shield"
                powerup_end_time = now + 999999
            powerup = None

        surface.fill(BLACK)
        if show_grid:
            draw_grid(surface)

        for ob in obstacles:
            ob.draw(surface)
        for f in food_list:
            f.draw(surface, font_small)
        if poison:
            poison.draw(surface, font_small)
        if powerup:
            powerup.draw(surface, font_small)
        snake.draw(surface, show_grid)

        score_s  = font.render(f"Score: {score}",        True, WHITE)
        level_s  = font.render(f"Level: {level}",        True, WHITE)
        best_s   = font_small.render(f"Best: {personal_best}", True, GRAY)
        surface.blit(score_s, (10, 10))
        surface.blit(level_s, (10, 40))
        surface.blit(best_s,  (10, 70))

        if active_powerup:
            t_left = max(0, (powerup_end_time - now) / 1000)
            pu_s = font_small.render(
                f"{active_powerup.upper()} {t_left:.1f}s" if active_powerup != "shield" else "SHIELD active",
                True, ORANGE
            )
            surface.blit(pu_s, (WIDTH - 160, 10))

        if snake.shield:
            sh_s = font_small.render("SHIELD", True, BLUE)
            surface.blit(sh_s, (WIDTH - 80, 30))

        pygame.display.flip()
        clock.tick(fps)

    return score, level