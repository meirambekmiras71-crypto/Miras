import pygame
import datetime
from tools import draw_shape, flood_fill, draw_toolbar

pygame.init()

WIDTH, HEIGHT = 900, 650
TOOLBAR_HEIGHT = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (200, 200, 200)
RED    = (255, 0, 0)
GREEN  = (0, 200, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN   = (0, 255, 255)
ORANGE = (255, 165, 0)

COLORS = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, ORANGE]
BRUSH_SIZES = [2, 5, 10]

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont(None, 22)
font_text = pygame.font.SysFont(None, 32)

mode = 'pencil'
color = BLACK
brush_size = BRUSH_SIZES[0]
start_pos = None
drawing = False
preview_canvas = None

text_active = False
text_pos = None
text_input = ''

prev_mouse_pos = None

SHAPE_MODES = {'rect', 'circle', 'square', 'rtri', 'etri', 'rhombus', 'line'}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if text_active:
                    text_active = False
                    text_input = ''
                else:
                    running = False

            keys = {
                pygame.K_p: 'pencil',
                pygame.K_l: 'line',
                pygame.K_r: 'rect',
                pygame.K_c: 'circle',
                pygame.K_s: 'square',
                pygame.K_t: 'rtri',
                pygame.K_y: 'etri',
                pygame.K_d: 'rhombus',
                pygame.K_e: 'eraser',
                pygame.K_f: 'fill',
                pygame.K_x: 'text',
            }
            if event.key in keys and not text_active:
                mode = keys[event.key]

            if not text_active:
                if event.key == pygame.K_1:
                    brush_size = BRUSH_SIZES[0]
                elif event.key == pygame.K_2:
                    brush_size = BRUSH_SIZES[1]
                elif event.key == pygame.K_3:
                    brush_size = BRUSH_SIZES[2]

            ctrl = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]
            if event.key == pygame.K_s and ctrl and not text_active:
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pygame.image.save(canvas, f"canvas_{ts}.png")

            if text_active:
                if event.key == pygame.K_RETURN:
                    surf = font_text.render(text_input, True, color)
                    canvas.blit(surf, text_pos)
                    text_active = False
                    text_input = ''
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    if event.unicode:
                        text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my < TOOLBAR_HEIGHT:
                for i, c in enumerate(COLORS):
                    x = WIDTH - len(COLORS) * 32 + i * 32
                    if x <= mx <= x + 28:
                        color = c
                for i, sz in enumerate(BRUSH_SIZES):
                    x = 5 + i * 40
                    if x <= mx <= x + 35 and 42 <= my <= 56:
                        brush_size = sz
            else:
                canvas_y = my - TOOLBAR_HEIGHT
                if mode == 'fill':
                    flood_fill(canvas, (mx, canvas_y), color)
                elif mode == 'text':
                    text_active = True
                    text_pos = (mx, canvas_y)
                    text_input = ''
                elif mode in SHAPE_MODES:
                    start_pos = (mx, canvas_y)
                    drawing = True
                    preview_canvas = canvas.copy()
                else:
                    prev_mouse_pos = (mx, canvas_y)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and start_pos:
                mx, my = event.pos
                canvas_y = my - TOOLBAR_HEIGHT
                draw_shape(canvas, mode, start_pos, (mx, canvas_y), color, brush_size)
                drawing = False
                start_pos = None
                preview_canvas = None
            prev_mouse_pos = None

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            canvas_y = my - TOOLBAR_HEIGHT
            if my > TOOLBAR_HEIGHT:
                if mode in ('pencil', 'eraser') and pygame.mouse.get_pressed()[0]:
                    draw_col = WHITE if mode == 'eraser' else color
                    if prev_mouse_pos:
                        pygame.draw.line(canvas, draw_col, prev_mouse_pos, (mx, canvas_y), brush_size)
                    prev_mouse_pos = (mx, canvas_y)
                else:
                    prev_mouse_pos = None

    screen.fill(GRAY)
    draw_toolbar(screen, mode, brush_size, color, COLORS, BRUSH_SIZES, font, TOOLBAR_HEIGHT, WIDTH)

    if drawing and preview_canvas and start_pos:
        temp = preview_canvas.copy()
        mx, my = pygame.mouse.get_pos()
        canvas_y = my - TOOLBAR_HEIGHT
        draw_shape(temp, mode, start_pos, (mx, canvas_y), color, brush_size)
        screen.blit(temp, (0, TOOLBAR_HEIGHT))
    else:
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if text_active and text_pos:
        preview = font_text.render(text_input + '|', True, color)
        screen.blit(preview, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()