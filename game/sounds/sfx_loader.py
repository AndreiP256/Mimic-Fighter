import pygame
from config.game_settings import SFX_DICT, MUSIC_PATH
from sounds.sound_manager import SoundManager

def load_sfx():
    sound_manager = SoundManager()
    sound_manager.load_music(MUSIC_PATH)
    for sound_name, sound_path in SFX_DICT.items():
        sound_manager.load_sound(sound_name, sound_path)