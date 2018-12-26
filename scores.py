import random

import pygame

import config


class Scoreboard(pygame.sprite.Sprite):


	images = None
	@staticmethod
	def __load_images(size):
		""" size = width of sprites """
		l = list()
		for x in range(0,10):
			l.append(pygame.Rect(x*size, 4*size, size, size))
		Scoreboard.sprites = l
		
		k = list()
		for digit in l:
			k.append(config.tileset_image.subsurface(digit))
		Scoreboard.images = k

	tiles = None
	@staticmethod
	def __load_tiles(size):
		l = list()
		r = pygame.Rect(0, 0, size, size)
		for x in range(0, 10):
			l.append(config.tileset_image.subsurface(r))
			r.x += size
		Scoreboard.tiles = l

	num_digits = 6

	def __init__(self, position, start_score=0, border_gfx=-1):
		ss = config.sprite_size
		if Scoreboard.images == None:
			Scoreboard.__load_images(ss)
		if Scoreboard.tiles == None:
			Scoreboard.__load_tiles(ss)

		super(Scoreboard, self).__init__()
		size = ((Scoreboard.num_digits+2)*ss, 3*ss)
		self.image = pygame.Surface(size)

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

		self.score = start_score
		self.digits = None
		
		self.gfx = border_gfx
		if self.gfx == -1:
			self.gfx = random.randint(0, 5)
		self.__decorate(ss)


	def __decorate(self, size):
		self.decour = list()
		""" top row of border decour """
		r = pygame.Rect(0,0,size,size)
		for x in range(0,self.rect.w/size):
			rc = r.copy()
			self.decour.append(rc)
			r.x += size
		""" sides of border decour """
		r.y += size
		r.x -= size
		self.decour.append(r.copy())
		r.x = 0
		self.decour.append(r.copy())
		""" bottom row of border decour """
		r.y += size
		for x in range(0,self.rect.w/size):
			rc = r.copy()
			self.decour.append(rc)
			r.x += size




	def update(self):
		if self.score == 0:
			for n in range(0, Scoreboard.num_digits):
				self.digits.append(0)
			return
		""" separating digits in our score """
		l = list()
		remainder = self.score
		while remainder > 0:
			k = remainder % 10 # our current digit
			remainder -= k
			remainder /= 10
			l = [k] + l
		while len(l) < Scoreboard.num_digits:
			l = [0] + l
		self.digits = l
		""" should add code for negative score """
		# riiiiight about here ;o

	def draw(self, screen):
		for rect in self.decour:
			self.image.blit(Scoreboard.tiles[self.gfx], rect)
		self.draw_digits(screen)
		screen.blit(self.image, self.rect)

	def draw_digits(self, screen):
		ss = config.sprite_size
		c = 0
		r = pygame.Rect(ss, ss, ss, ss)
		while c < Scoreboard.num_digits:
			self.image.blit(Scoreboard.images[self.digits[c]], r)
			r.x += ss
			c += 1
		