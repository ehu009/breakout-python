import pygame
import config
import vector


racket_image = pygame.image.load(config.image_paths[1])


class Paddle (pygame.sprite.Sprite):

	def __init__(self):
		ss = config.sprite_size
		super(Paddle, self).__init__()
		y = config.play_size.h -3*ss
		x = config.play_size.x

		self.pos = vector.Vector2D(x, y)
		self.vel = vector.Vector2D(0, 0)
		self.rect = pygame.Rect(x, y, 6*ss, 2*ss)
		self.image = racket_image
	
	
	def draw(self, screen):
		screen.blit(self.image, self.rect)
	
	def update(self, time, x_input):
		def_speed = 0.3
		ps = config.play_size
		
		self.vel.x = 0
		if self.pos.x > ps.x:
			if x_input < 0:
				""" move to the left """
				self.vel.x = -def_speed
		if self.pos.x < ps.x + ps.w - config.sprite_size*6:
			if x_input > 0:
				""" move to the right """
				self.vel.x = def_speed
		
		self.pos.x += self.vel.x*time
		self.rect.x = self.pos.x


