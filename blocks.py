import random

import pygame

import config



group = pygame.sprite.Group()


class Block (pygame.sprite.Sprite):
	
	def __init__(self, position, frame=-1):
		super(Block, self).__init__()
		ss = config.sprite_size
		r = pygame.Rect(0, 0, ss,ss)
		x = frame
		if x == -1:
			x = random.randint(0,6)
		r.x = x * ss
		self.image = config.tileset_image.subsurface(r)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]







	

