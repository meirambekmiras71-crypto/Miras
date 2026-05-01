import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'paint'
    color_choice = (0, 0, 255)

    points = []

    start_pos = None
    drawing_shape = False

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_1:
                    color_choice = (255, 0, 0)
                elif event.key == pygame.K_2:
                    color_choice = (0, 255, 0)
                elif event.key == pygame.K_3:
                    color_choice = (0, 0, 255)
                elif event.key == pygame.K_4:
                    color_choice = (255, 255, 0)

                if event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_p:
                    mode = 'paint'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_t:
                    mode = 'right_triangle'
                elif event.key == pygame.K_y:
                    mode = 'eq_triangle'
                elif event.key == pygame.K_d:
                    mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mode in ['rect', 'circle', 'square', 'right_triangle', 'eq_triangle', 'rhombus']:
                        start_pos = event.pos
                        drawing_shape = True
                    else:
                        radius = min(200, radius + 1)
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing_shape:
                    end_pos = event.pos
                    points.append({'type': mode, 'start': start_pos, 'end': end_pos, 'color': color_choice})
                    drawing_shape = False

            if event.type == pygame.MOUSEMOTION:
                if mode in ['paint', 'eraser']:
                    if pygame.mouse.get_pressed()[0]:
                        color = (0, 0, 0) if mode == 'eraser' else color_choice
                        points.append({'type': 'line', 'pos': event.pos, 'radius': radius, 'color': color})

        screen.fill((0, 0, 0))

        for p in points:
            if p['type'] == 'line':
                pygame.draw.circle(screen, p['color'], p['pos'], p['radius'])
            elif p['type'] == 'rect':
                draw_rectangle(screen, p['start'], p['end'], p['color'])
            elif p['type'] == 'circle':
                draw_circle(screen, p['start'], p['end'], p['color'])
            elif p['type'] == 'square':
                draw_square(screen, p['start'], p['end'], p['color'])
            elif p['type'] == 'right_triangle':
                draw_right_triangle(screen, p['start'], p['end'], p['color'])
            elif p['type'] == 'eq_triangle':
                draw_eq_triangle(screen, p['start'], p['end'], p['color'])
            elif p['type'] == 'rhombus':
                draw_rhombus(screen, p['start'], p['end'], p['color'])

        if drawing_shape:
            current_pos = pygame.mouse.get_pos()
            if mode == 'rect':
                draw_rectangle(screen, start_pos, current_pos, color_choice)
            elif mode == 'circle':
                draw_circle(screen, start_pos, current_pos, color_choice)
            elif mode == 'square':
                draw_square(screen, start_pos, current_pos, color_choice)
            elif mode == 'right_triangle':
                draw_right_triangle(screen, start_pos, current_pos, color_choice)
            elif mode == 'eq_triangle':
                draw_eq_triangle(screen, start_pos, current_pos, color_choice)
            elif mode == 'rhombus':
                draw_rhombus(screen, start_pos, current_pos, color_choice)

        pygame.display.flip()
        clock.tick(60)


def draw_rectangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), width, height), 2)


def draw_circle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    radius = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    pygame.draw.circle(screen, color, start, radius, 2)


def draw_square(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x1 - x2), abs(y1 - y2))
    sign_x = 1 if x2 >= x1 else -1
    sign_y = 1 if y2 >= y1 else -1
    pygame.draw.rect(screen, color, (x1, y1, side * sign_x, side * sign_y), 2)


def draw_right_triangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    p1 = (x1, y1)
    p2 = (x1, y2)
    p3 = (x2, y2)
    pygame.draw.polygon(screen, color, [p1, p2, p3], 2)


def draw_eq_triangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    side = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    cx = (x1 + x2) / 2
    height = math.sqrt(3) / 2 * side
    p1 = (x1, y2)
    p2 = (x2, y2)
    p3 = (int(cx), int(y2 - height))
    pygame.draw.polygon(screen, color, [p1, p2, p3], 2)


def draw_rhombus(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    p1 = (cx, y1)
    p2 = (x2, cy)
    p3 = (cx, y2)
    p4 = (x1, cy)
    pygame.draw.polygon(screen, color, [p1, p2, p3, p4], 2)


main()