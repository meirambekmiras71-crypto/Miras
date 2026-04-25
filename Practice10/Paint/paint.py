import pygame

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mode in ['rect', 'circle']:
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
                if mode == 'paint' or mode == 'eraser':
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

        if drawing_shape:
            current_pos = pygame.mouse.get_pos()
            if mode == 'rect':
                draw_rectangle(screen, start_pos, current_pos, color_choice)
            elif mode == 'circle':
                draw_circle(screen, start_pos, current_pos, color_choice)

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

main()