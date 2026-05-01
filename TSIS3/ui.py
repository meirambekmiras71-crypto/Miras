import pygame

BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (200, 200, 200)
DGRAY  = (100, 100, 100)
RED    = (255, 0, 0)
GREEN  = (0, 200, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 200, 0)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

font_large  = None
font_medium = None
font_small  = None


def init_fonts():
    global font_large, font_medium, font_small
    font_large  = pygame.font.SysFont("Verdana", 48)
    font_medium = pygame.font.SysFont("Verdana", 28)
    font_small  = pygame.font.SysFont("Verdana", 20)


def draw_button(surface, text, rect, active=False):
    color = DGRAY if active else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=8)
    label = font_medium.render(text, True, BLACK)
    lx = rect[0] + (rect[2] - label.get_width()) // 2
    ly = rect[1] + (rect[3] - label.get_height()) // 2
    surface.blit(label, (lx, ly))


def main_menu(surface):
    buttons = {
        "play":        pygame.Rect(100, 200, 200, 50),
        "leaderboard": pygame.Rect(100, 270, 200, 50),
        "settings":    pygame.Rect(100, 340, 200, 50),
        "quit":        pygame.Rect(100, 410, 200, 50),
    }
    labels = {
        "play":        "Play",
        "leaderboard": "Leaderboard",
        "settings":    "Settings",
        "quit":        "Quit",
    }

    while True:
        surface.fill(WHITE)
        title = font_large.render("RACER", True, RED)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 100))

        mx, my = pygame.mouse.get_pos()
        for key, rect in buttons.items():
            draw_button(surface, labels[key], rect, rect.collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key


def enter_username(surface):
    username = ""
    input_rect = pygame.Rect(80, 280, 240, 44)

    while True:
        surface.fill(WHITE)
        title = font_medium.render("Enter your name:", True, BLACK)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 200))

        pygame.draw.rect(surface, GRAY, input_rect, border_radius=6)
        pygame.draw.rect(surface, BLACK, input_rect, 2, border_radius=6)
        name_surf = font_medium.render(username + "|", True, BLACK)
        surface.blit(name_surf, (input_rect.x + 8, input_rect.y + 8))

        hint = font_small.render("Press Enter to start", True, DGRAY)
        surface.blit(hint, ((SCREEN_WIDTH - hint.get_width()) // 2, 340))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode and len(username) < 16:
                    username += event.unicode


def game_over_screen(surface, score, distance, coins):
    buttons = {
        "retry": pygame.Rect(60,  440, 120, 50),
        "menu":  pygame.Rect(220, 440, 120, 50),
    }

    while True:
        surface.fill(RED)
        title = font_large.render("Game Over", True, WHITE)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 80))

        lines = [
            f"Score:    {score}",
            f"Distance: {distance} m",
            f"Coins:    {coins}",
        ]
        for i, line in enumerate(lines):
            surf = font_medium.render(line, True, WHITE)
            surface.blit(surf, (60, 200 + i * 60))

        mx, my = pygame.mouse.get_pos()
        draw_button(surface, "Retry",     buttons["retry"], buttons["retry"].collidepoint(mx, my))
        draw_button(surface, "Main Menu", buttons["menu"],  buttons["menu"].collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key


def leaderboard_screen(surface, entries):
    back_btn = pygame.Rect(130, 540, 140, 44)

    while True:
        surface.fill(WHITE)
        title = font_large.render("Top 10", True, BLUE)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 20))

        header = font_small.render("  # Name            Score   Dist", True, DGRAY)
        surface.blit(header, (10, 75))
        pygame.draw.line(surface, DGRAY, (10, 95), (390, 95), 1)

        for i, e in enumerate(entries[:10]):
            line = f"{i+1:>2}. {e['name']:<12} {e['score']:<7} {e['distance']}m"
            surf = font_small.render(line, True, BLACK)
            surface.blit(surf, (10, 100 + i * 42))

        mx, my = pygame.mouse.get_pos()
        draw_button(surface, "Back", back_btn, back_btn.collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen(surface, settings):
    back_btn   = pygame.Rect(130, 540, 140, 44)
    sound_btn  = pygame.Rect(220, 150, 140, 40)
    color_btn  = pygame.Rect(220, 210, 140, 40)
    diff_btn   = pygame.Rect(220, 270, 140, 40)

    colors       = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        surface.fill(WHITE)
        title = font_large.render("Settings", True, BLACK)
        surface.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 60))

        sound_lbl = font_medium.render("Sound:", True, BLACK)
        color_lbl = font_medium.render("Car color:", True, BLACK)
        diff_lbl  = font_medium.render("Difficulty:", True, BLACK)
        surface.blit(sound_lbl, (30, 158))
        surface.blit(color_lbl, (30, 218))
        surface.blit(diff_lbl,  (30, 278))

        mx, my = pygame.mouse.get_pos()
        draw_button(surface, "ON" if settings["sound"] else "OFF", sound_btn, sound_btn.collidepoint(mx, my))
        draw_button(surface, settings["car_color"].capitalize(),    color_btn, color_btn.collidepoint(mx, my))
        draw_button(surface, settings["difficulty"].capitalize(),   diff_btn,  diff_btn.collidepoint(mx, my))
        draw_button(surface, "Back", back_btn, back_btn.collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return settings
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                elif color_btn.collidepoint(event.pos):
                    idx = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(idx + 1) % len(colors)]
                elif diff_btn.collidepoint(event.pos):
                    idx = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(idx + 1) % len(difficulties)]
                elif back_btn.collidepoint(event.pos):
                    return settings