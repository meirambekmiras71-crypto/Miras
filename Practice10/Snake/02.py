import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

CELL = 30
# Initialize font for score and level display
font = pygame.font.SysFont(None, 36)

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

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
        head = self.body[0]
        # Check if head hits the boundaries
        if head.x > WIDTH // CELL - 1 or head.x < 0 or head.y > HEIGHT // CELL - 1 or head.y < 0:
            return True
        # Check if head hits its own body
        for i in range(1, len(self.body)):
            if head.x == self.body[i].x and head.y == self.body[i].y:
                return True
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_food_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            # Grow the snake and relocate food
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos(self.body)
            return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body):
        # Keep generating a new position until it doesn't overlap with the snake
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            on_snake = False
            for segment in snake_body:
                if self.pos.x == segment.x and self.pos.y == segment.y:
                    on_snake = True
                    break
            if not on_snake:
                break

# Game settings and state
FPS = 5
clock = pygame.time.Clock()
score = 0
level = 1
foods_to_level_up = 3

food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Added direction checks to prevent 180-degree turns into self
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

    screen.fill(colorBLACK)
    draw_grid()

    snake.move()
    
    # End game if collision detected
    if snake.check_collision_with_walls_and_self():
        running = False

    # Handle eating food and level progression
    if snake.check_food_collision(food):
        score += 1
        if score % foods_to_level_up == 0:
            level += 1
            FPS += 2 # Increase speed with each level

    snake.draw()
    food.draw()

    # Render score and level UI
    score_surf = font.render(f"Score: {score}", True, colorWHITE)
    level_surf = font.render(f"Level: {level}", True, colorWHITE)
    screen.blit(score_surf, (10, 10))
    screen.blit(level_surf, (10, 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()