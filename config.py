
import os
import pygame


demo = False

""" Images and their paths """
image_paths = ("tileset.png","player.png", "ball.png")
paths = []
for p in image_paths:
    paths.append(os.path.join("img", p))
image_paths = paths
#

""" Tiled things """
sprite_size = 8
tileset_image = pygame.image.load(image_paths[0])


""" Ball stuff """
ball_size = 24
ball_image = pygame.image.load(image_paths[2])

""" asdfsdaadsfa CLEAN ME UP DADDY """
play_area_ratio = (5, 3)
play_area_scale = 12


border_thickness = 8

play_size = pygame.Rect(0, 0, play_area_ratio[0]*sprite_size*play_area_scale, play_area_ratio[1]*sprite_size*play_area_scale)
border_size = (sprite_size * border_thickness, play_size.h)


play_size.x = border_size[0]
screen_size = (play_size.w + 2*border_size[0], play_size.h)
