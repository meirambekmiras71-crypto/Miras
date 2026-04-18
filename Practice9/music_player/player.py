import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.tracks = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        self.tracks.sort()
        self.folder = music_folder
        self.index = 0
        self.playing = False

    def play(self):
        if not self.tracks:
            return
        pygame.mixer.music.load(os.path.join(self.folder, self.tracks[self.index]))
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def prev_track(self):
        self.index = (self.index - 1) % len(self.tracks)
        self.play()

    def current_track(self):
        if self.tracks:
            return self.tracks[self.index]
        return "No tracks"