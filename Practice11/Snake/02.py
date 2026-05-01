import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

CELL = 30
font = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)


def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"


class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_collision_with_walls_and_self(self):
        # Check if head hits boundaries or own body
        head = self.body[0]
        if head.x > WIDTH // CELL - 1 or head.x < 0 or head.y > HEIGHT // CELL - 1 or head.y < 0:
            return True
        for i in range(1, len(self.body)):
            if head.x == self.body[i].x and head.y == self.body[i].y:
                return True
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_food_collision(self, food_list):
        # Check if snake head collides with any food item
        head = self.body[0]
        for food in food_list:
            if head.x == food.pos.x and head.y == food.pos.y:
                self.body.append(Point(head.x, head.y))
                return food
        return None


class Food:
    # Food types: (value, color, lifetime_seconds or None)
    TYPES = [
        (1,  colorGREEN,  None),
        (3,  colorBLUE,   7),
        (5,  colorWHITE,  4),
    ]

    def __init__(self, snake_body, all_food):
        # Randomly select food type based on weights
        weights = [60, 30, 10]
        chosen = random.choices(self.TYPES, weights=weights, k=1)[0]
        self.value = chosen[0]
        self.color = chosen[1]
        self.lifetime = chosen[2]
        self.spawn_time = pygame.time.get_ticks()
        self.pos = Point(0, 0)
        self.generate_random_pos(snake_body, all_food)

    def is_expired(self):
        # Check if food has exceeded its lifetime
        if self.lifetime is None:
            return False
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000
        return elapsed >= self.lifetime

    def time_left(self):
        # Return remaining time for temporary food
        if self.lifetime is None:
            return None
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000
        return max(0, self.lifetime - elapsed)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        # Show value label on food
        label = font_small.render(str(self.value), True, colorBLACK)
        screen.blit(label, (self.pos.x * CELL + 6, self.pos.y * CELL + 6))
        # Show timer for temporary food
        if self.lifetime is not None:
            t = self.time_left()
            timer_label = font_small.render(f"{t:.1f}", True, colorRED)
            screen.blit(timer_label, (self.pos.x * CELL, self.pos.y * CELL - 16))

    def generate_random_pos(self, snake_body, all_food):
        # Generate position that doesn't overlap with snake or other food
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            on_snake = any(s.x == x and s.y == y for s in snake_body)
            on_food = any(f.pos.x == x and f.pos.y == y for f in all_food)
            if not on_snake and not on_food:
                self.pos.x = x
                self.pos.y = y
                break


FPS = 5
clock = pygame.time.Clock()
score = 0
level = 1
foods_to_level_up = 3

snake = Snake()
food_list = [Food(snake.body, [])]

SPAWN_BONUS_FOOD = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_BONUS_FOOD, 5000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1
        if event.type == SPAWN_BONUS_FOOD:
            # Spawn a new bonus food every 5 seconds (max 3 food items at once)
            if len(food_list) < 3:
                food_list.append(Food(snake.body, food_list))

    # Remove expired food items
    food_list = [f for f in food_list if not f.is_expired()]

    # Ensure at least one food is always present
    if not food_list:
        food_list.append(Food(snake.body, []))

    screen.fill(colorBLACK)
    draw_grid()

    snake.move()

    if snake.check_collision_with_walls_and_self():
        running = False

    eaten = snake.check_food_collision(food_list)
    if eaten:
        score += eaten.value
        food_list.remove(eaten)
        food_list.append(Food(snake.body, food_list))
        if score % foods_to_level_up == 0:
            level += 1
            FPS += 2

    for food in food_list:
        food.draw()

    snake.draw()

    score_surf = font.render(f"Score: {score}", True, colorWHITE)
    level_surf = font.render(f"Level: {level}", True, colorWHITE)
    screen.blit(score_surf, (10, 10))
    screen.blit(level_surf, (10, 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()