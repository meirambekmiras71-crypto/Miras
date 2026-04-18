import pygame
import os
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

music_folder = os.path.join(os.path.dirname(__file__), "music")
player = MusicPlayer(music_folder)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((30, 30, 30))

    track_text = font.render(f"Track: {player.current_track()}", True, (255, 255, 255))
    status_text = font.render(f"Status: {'Playing' if player.playing else 'Stopped'}", True, (0, 255, 0) if player.playing else (255, 0, 0))
    controls = small_font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, (180, 180, 180))

    screen.blit(track_text, (50, 150))
    screen.blit(status_text, (50, 200))
    screen.blit(controls, (50, 320))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()