import pygame
import math
from collections import deque


def draw_shape(surface, shape, start, end, color, size):
    x1, y1 = start
    x2, y2 = end
    if shape == 'rect':
        w, h = abs(x2 - x1), abs(y2 - y1)
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), w, h), size)
    elif shape == 'circle':
        r = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start, r, size)
    elif shape == 'square':
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = 1 if x2 >= x1 else -1
        sy = 1 if y2 >= y1 else -1
        pygame.draw.rect(surface, color, (x1, y1, side * sx, side * sy), size)
    elif shape == 'rtri':
        pygame.draw.polygon(surface, color, [(x1, y1), (x1, y2), (x2, y2)], size)
    elif shape == 'etri':
        side = math.hypot(x2 - x1, y2 - y1)
        cx = (x1 + x2) / 2
        h = math.sqrt(3) / 2 * side
        pygame.draw.polygon(surface, color, [(x1, y2), (x2, y2), (int(cx), int(y2 - h))], size)
    elif shape == 'rhombus':
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        pygame.draw.polygon(surface, color, [(cx, y1), (x2, cy), (cx, y2), (x1, cy)], size)
    elif shape == 'line':
        pygame.draw.line(surface, color, start, end, size)


def flood_fill(surface, pos, fill_color):
    x, y = pos
    target = surface.get_at((x, y))[:3]
    if target == fill_color:
        return
    queue = deque()
    queue.append((x, y))
    visited = set()
    w, h = surface.get_size()
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) in visited:
            continue
        if cx < 0 or cx >= w or cy < 0 or cy >= h:
            continue
        if surface.get_at((cx, cy))[:3] != target:
            continue
        surface.set_at((cx, cy), fill_color)
        visited.add((cx, cy))
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))


def draw_toolbar(screen, mode, brush_size, color, colors, brush_sizes, font, toolbar_height, width):
    GRAY  = (200, 200, 200)
    DGRAY = (150, 150, 150)
    BLACK = (0, 0, 0)

    pygame.draw.rect(screen, GRAY, (0, 0, width, toolbar_height))

    tools = [
        ('pencil', 'P'),
        ('line',   'L'),
        ('rect',   'R'),
        ('circle', 'C'),
        ('square', 'S'),
        ('rtri',   'T'),
        ('etri',   'Y'),
        ('rhombus','D'),
        ('eraser', 'E'),
        ('fill',   'F'),
        ('text',   'X'),
    ]

    for i, (tool, label) in enumerate(tools):
        x = 5 + i * 72
        color_btn = DGRAY if mode == tool else GRAY
        pygame.draw.rect(screen, color_btn, (x, 8, 65, 30), border_radius=4)
        pygame.draw.rect(screen, BLACK,     (x, 8, 65, 30), 1, border_radius=4)
        txt = font.render(f"{label}:{tool[:4]}", True, BLACK)
        screen.blit(txt, (x + 4, 16))

    for i, sz in enumerate(brush_sizes):
        x = 5 + i * 40
        y = 42
        active = sz == brush_size
        pygame.draw.rect(screen, DGRAY if active else GRAY, (x, y, 35, 14), border_radius=3)
        pygame.draw.rect(screen, BLACK, (x, y, 35, 14), 1, border_radius=3)
        lbl = font.render(f"{sz}px", True, BLACK)
        screen.blit(lbl, (x + 4, y + 2))

    for i, c in enumerate(colors):
        x = width - len(colors) * 32 + i * 32
        pygame.draw.rect(screen, c, (x, 10, 28, 40))
        if c == color:
            pygame.draw.rect(screen, BLACK, (x, 10, 28, 40), 3)