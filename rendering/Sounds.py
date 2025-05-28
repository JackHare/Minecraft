import pygame

SOUNDS = {
    "ambient" : './rendering/sounds/Earth.ogg',
    "run_grass/dirt" : './rendering/sounds/grass-dirt-run.ogg',
    "run_blocks" : './rendering/sounds/iron-diamond-gold-coal-run.ogg',
    "run_stone" : './rendering/sounds/stone-ore-cobble-run.ogg',
    "mine_grass/dirt" : './rendering/sounds/grass-dirt-mine.ogg',
    "mine_blocks" : './rendering/sounds/iron-stone-diamond-goal-coal-ore-cobble-mine.ogg',
}
class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        for sound_name, sound_path in SOUNDS.items():
            self.sounds[sound_name] = pygame.mixer.Sound(sound_path)

    def play_ambient(self):
        """Play ambient background sound."""
        self.sounds["ambient"].play(-1)

    def play_run(self, surface_type):
        """Play running sound based on surface type."""
        sound_key = f"run_{surface_type}"
        if sound_key in self.sounds:
            self.sounds[sound_key].play()

    def play_mine(self, surface_type):
        """Play mining sound based on surface type."""
        sound_key = f"mine_{surface_type}"
        if sound_key in self.sounds:
            self.sounds[sound_key].play()

    def stop_all(self):
        """Stop all playing sounds."""
        pygame.mixer.stop()
