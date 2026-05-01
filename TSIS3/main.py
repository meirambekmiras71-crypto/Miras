import pygame
import sys
from ui import (
    init_fonts,
    main_menu,
    enter_username,
    game_over_screen,
    leaderboard_screen,
    settings_screen,
)
from racer import run_game
from persistence import (
    load_settings,
    save_settings,
    load_leaderboard,
    add_leaderboard_entry,
)

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

init_fonts()

settings = load_settings()
username = None

while True:
    action = main_menu(surface)

    if action == "quit":
        pygame.quit()
        sys.exit()

    elif action == "leaderboard":
        entries = load_leaderboard()
        leaderboard_screen(surface, entries)

    elif action == "settings":
        settings = settings_screen(surface, settings)
        save_settings(settings)

    elif action == "play":
        username = enter_username(surface)
        if username is None:
            pygame.quit()
            sys.exit()

        while True:
            result, score, distance, coins = run_game(surface, settings, username)

            if result == "quit":
                pygame.quit()
                sys.exit()

            if result == "gameover":
                add_leaderboard_entry(username, score, distance, coins)
                action = game_over_screen(surface, score, distance, coins)

                if action == "quit":
                    pygame.quit()
                    sys.exit()
                elif action == "retry":
                    continue
                elif action == "menu":
                    break

            elif result == "menu":
                break