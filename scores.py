import pygame

import config


class Scoreboard(pygame.sprite.Sprite):


	images = None
	@staticmethod
	def __load_images(size):
		""" size = width of sprites """
		l = list()
		for x in range(0,9):
			l.append(pygame.Rect(x*size, 4*size, size, size))
		Scoreboard.sprites = l
		
		k = list()
		for digit in l:
			k.append(config.tileset_image.subsurface(digit))
		Scoreboard.images = k


	num_digits = 6

	def __init__(self, position, start_score=0):
		ss = config.sprite_size
		if Scoreboard.images == None:
			Scoreboard.__load_images(ss)
			
		super(Scoreboard, self).__init__()
		size = (Scoreboard.num_digits*ss, Scoreboard.num_digits*ss)
		self.image = pygame.Surface(size)
		self.rect = self.image.get_rect()

		self.rect.x = position.x
		self.rect.y = position.y

		self.score = start_score
		self.digits = None
		

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
		ss = config.sprite_size
		c = 0
		r = pygame.Rect(0, 0, ss, ss)
		while c < Scoreboard.num_digits:
			self.image.blit(Scoreboard.images[self.digits[c]], r)
			r.x += ss
			c += 1
		screen.blit(self.image, self.rect)