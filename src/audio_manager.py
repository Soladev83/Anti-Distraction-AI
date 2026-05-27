import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Quiet the console print
import pygame

class AudioManager:
    def __init__(self, audio_path="assets/scream.mp3"):
        pygame.mixer.init()
        self.audio_path = audio_path
        self.is_playing = False

        if not os.path.exists(self.audio_path):
            print(f"[Warning] Audio file not found at {self.audio_path}. Please add it.")

    def play_alarm(self):
        """Plays the alarm audio if it's not already playing."""
        if os.path.exists(self.audio_path) and not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load(self.audio_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing audio: {e}")

    def stop_alarm(self):
        """Stops the alarm audio if it is playing."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()