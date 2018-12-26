
import os
import pygame


demo = False

def full_paths (dir, names):
    l = []
    for name in names:
        l.append(os.path.join(dir, name))
    return l


""" Images and their paths """
image_paths = full_paths("img", ("tileset.png","player.png", "ball.png"))

""" Sounds and their paths """
snd_name = ("ball.wav", "beep.wav", "pit.wav", "loss.wav", "victory.wav")
volumes = (0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12)
sound_paths = full_paths("snd", snd_name)

sounds = dict()
def load_sounds():
    c = 0
    for p in sound_paths:
        key = snd_name[c]
        value = pygame.mixer.Sound(p)
        value.set_volume(volumes[c])
        sounds[key] = value
        c += 1
"""        
    pygame.mixer.Sound(config.sound_paths[2])
	woof_snd.set_volume(0.12)

	boop_snd = pygame.mixer.Sound(config.sound_paths[1])
	boop_snd.set_volume(0.12)
	config.sounds.append(boop_snd)
	config.sounds.append(woof_snd)
"""


""" Tiled things """
sprite_size = 8
tileset_image = pygame.image.load(image_paths[0])


""" Ball stuff """
ball_size = 24
ball_image = pygame.image.load(image_paths[2])


""" Player restrictions """
firing_interval = 300


""" asdfsdaadsfa CLEAN ME UP DADDY """
play_area_ratio = (5, 3)
play_area_scale = 12


border_thickness = 8

play_size = pygame.Rect(0, 0, play_area_ratio[0]*sprite_size*play_area_scale, play_area_ratio[1]*sprite_size*play_area_scale)
border_size = (sprite_size * border_thickness, play_size.h)


play_size.x = border_size[0]
screen_size = (play_size.w + 2*border_size[0], play_size.h)
