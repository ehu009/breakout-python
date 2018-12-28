import random

import pygame

import config


graphic_group = pygame.sprite.Group()

class Graphic (pygame.sprite.Sprite):
	
	def __init__(self, position, frame=-1):
		super(Graphic, self).__init__()
		ss = config.sprite_size
		r = pygame.Rect(0, 0, ss, ss)
		x = frame
		if x == -1:
			x = random.randint(0, 5)
		
		r.x = x * ss


		self.image = config.tileset_image.subsurface(r)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]
