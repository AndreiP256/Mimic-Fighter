import pygame

class SoundManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SoundManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, music_volume=0.5, sfx_volume=0.5):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            pygame.mixer.init()
            self.music_volume = music_volume
            self.sfx_volume = sfx_volume
            self.sounds = {}
            self.initialized = True

    def load_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.music_volume)

    def play_music(self, loops=-1):
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def load_sound(self, sound_name, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(self.sfx_volume)
        self.sounds[sound_name] = sound

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)