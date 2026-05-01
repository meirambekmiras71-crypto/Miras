import pygame
import sys
import json
import os
from config import *
from db import init_db, get_or_create_player, save_session, get_top10, get_personal_best
from game import run_game

pygame.init()

surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

font_large  = pygame.font.SysFont(None, 64)
font_medium = pygame.font.SysFont(None, 36)
font_small  = pygame.font.SysFont(None, 24)

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "snake_color": list(YELLOW),
    "grid":        True,
    "sound":       True,
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    with open(SETTINGS_FILE) as f:
        data = json.load(f)
    for k, v in DEFAULT_SETTINGS.items():
        if k not in data:
            data[k] = v
    return data


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def draw_button(rect, text, hover=False):
    color = DGRAY if hover else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=8)
    lbl = font_medium.render(text, True, BLACK)
    surface.blit(lbl, (rect.x + (rect.w - lbl.get_width()) // 2,
                        rect.y + (rect.h - lbl.get_height()) // 2))


def main_menu():
    buttons = {
        "play":        pygame.Rect(200, 200, 200, 50),
        "leaderboard": pygame.Rect(200, 270, 200, 50),
        "settings":    pygame.Rect(200, 340, 200, 50),
        "quit":        pygame.Rect(200, 410, 200, 50),
    }
    labels = {
        "play":        "Play",
        "leaderboard": "Leaderboard",
        "settings":    "Settings",
        "quit":        "Quit",
    }
    while True:
        surface.fill(BLACK)
        title = font_large.render("SNAKE", True, GREEN)
        surface.blit(title, ((WIDTH - title.get_width()) // 2, 100))
        mx, my = pygame.mouse.get_pos()
        for key, rect in buttons.items():
            draw_button(rect, labels[key], rect.collidepoint(mx, my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key


def enter_username():
    username = ""
    input_rect = pygame.Rect(150, 280, 300, 44)
    while True:
        surface.fill(BLACK)
        title = font_medium.render("Enter your name:", True, WHITE)
        surface.blit(title, ((WIDTH - title.get_width()) // 2, 200))
        pygame.draw.rect(surface, GRAY, input_rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, input_rect, 2, border_radius=6)
        name_s = font_medium.render(username + "|", True, BLACK)
        surface.blit(name_s, (input_rect.x + 8, input_rect.y + 8))
        hint = font_small.render("Press Enter to start", True, DGRAY)
        surface.blit(hint, ((WIDTH - hint.get_width()) // 2, 340))
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


def game_over_screen(score, level, personal_best):
    buttons = {
        "retry": pygame.Rect(100, 440, 160, 50),
        "menu":  pygame.Rect(340, 440, 160, 50),
    }
    while True:
        surface.fill(BLACK)
        title = font_large.render("Game Over", True, RED)
        surface.blit(title, ((WIDTH - title.get_width()) // 2, 80))
        lines = [
            f"Score:    {score}",
            f"Level:    {level}",
            f"Best:     {personal_best}",
        ]
        for i, line in enumerate(lines):
            s = font_medium.render(line, True, WHITE)
            surface.blit(s, (150, 200 + i * 60))
        mx, my = pygame.mouse.get_pos()
        draw_button(buttons["retry"], "Retry",     buttons["retry"].collidepoint(mx, my))
        draw_button(buttons["menu"],  "Main Menu", buttons["menu"].collidepoint(mx, my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key


def leaderboard_screen():
    back_btn = pygame.Rect(220, 540, 160, 44)
    entries  = get_top10()
    while True:
        surface.fill(BLACK)
        title = font_large.render("Top 10", True, YELLOW)
        surface.blit(title, ((WIDTH - title.get_width()) // 2, 20))
        header = font_small.render("  # Username         Score  Level  Date", True, GRAY)
        surface.blit(header, (10, 80))
        pygame.draw.line(surface, GRAY, (10, 100), (590, 100), 1)
        for i, row in enumerate(entries):
            name, score, level, played_at = row
            date_str = played_at.strftime("%Y-%m-%d") if played_at else ""
            line = f"{i+1:>2}. {name:<14} {score:<7} {level:<6} {date_str}"
            s = font_small.render(line, True, WHITE)
            surface.blit(s, (10, 108 + i * 40))
        mx, my = pygame.mouse.get_pos()
        draw_button(back_btn, "Back", back_btn.collidepoint(mx, my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen(settings):
    back_btn   = pygame.Rect(220, 540, 160, 44)
    grid_btn   = pygame.Rect(350, 180, 160, 40)
    sound_btn  = pygame.Rect(350, 240, 160, 40)
    color_btn  = pygame.Rect(350, 300, 160, 40)

    colors = [
        ("Yellow", list(YELLOW)),
        ("Green",  list(GREEN)),
        ("Blue",   list(BLUE)),
        ("Orange", list(ORANGE)),
        ("Purple", list(PURPLE)),
    ]
    color_names = [c[0] for c in colors]
    color_values = [c[1] for c in colors]

    def current_color_name():
        for name, val in colors:
            if val == settings["snake_color"]:
                return name
        return "Custom"

    while True:
        surface.fill(BLACK)
        title = font_large.render("Settings", True, WHITE)
        surface.blit(title, ((WIDTH - title.get_width()) // 2, 80))

        for label, rect, val in [
            ("Grid:",        grid_btn,  "ON" if settings["grid"]  else "OFF"),
            ("Sound:",       sound_btn, "ON" if settings["sound"] else "OFF"),
            ("Snake color:", color_btn, current_color_name()),
        ]:
            lbl = font_medium.render(label, True, WHITE)
            surface.blit(lbl, (80, rect.y + 8))

        mx, my = pygame.mouse.get_pos()
        draw_button(grid_btn,  "ON" if settings["grid"]  else "OFF", grid_btn.collidepoint(mx, my))
        draw_button(sound_btn, "ON" if settings["sound"] else "OFF", sound_btn.collidepoint(mx, my))
        draw_button(color_btn, current_color_name(),                  color_btn.collidepoint(mx, my))
        draw_button(back_btn,  "Save & Back",                         back_btn.collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return settings
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                elif color_btn.collidepoint(event.pos):
                    idx = color_values.index(settings["snake_color"]) if settings["snake_color"] in color_values else 0
                    settings["snake_color"] = color_values[(idx + 1) % len(color_values)]
                elif back_btn.collidepoint(event.pos):
                    return settings


init_db()
settings  = load_settings()
username  = None
player_id = None

while True:
    action = main_menu()

    if action == "quit":
        pygame.quit()
        sys.exit()

    elif action == "leaderboard":
        leaderboard_screen()

    elif action == "settings":
        settings = settings_screen(settings)
        save_settings(settings)

    elif action == "play":
        username = enter_username()
        if username is None:
            pygame.quit()
            sys.exit()

        player_id     = get_or_create_player(username)
        personal_best = get_personal_best(player_id)

        while True:
            score, level = run_game(surface, settings, player_id, personal_best)
            save_session(player_id, score, level)
            personal_best = max(personal_best, score)

            action = game_over_screen(score, level, personal_best)
            if action == "quit":
                pygame.quit()
                sys.exit()
            elif action == "retry":
                continue
            elif action == "menu":
                break