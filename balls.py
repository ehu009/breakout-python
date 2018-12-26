import pygame

import config
import vector
import animate


group = pygame.sprite.Group()


size = config.ball_size
arena = config.play_size



class Ball (pygame.sprite.Sprite):
	
	group = pygame.sprite.Group()
	sprites = None
	animation = None
	ttn = 40

	@staticmethod
	def __load_graphics():
		l = list()
		for x in range (0,4):
			l.append((size*x,0, size, size))
		Ball.sprites = l
		Ball.animation = animate.Sequenced(config.ball_image, Ball.sprites)

	def __init__(self, position, velocity):
		if Ball.sprites == None:
			Ball.__load_graphics()

		super(Ball, self).__init__()
		
		self.animation = Ball.animation

		self.image = self.animation[0]
		self.rect = self.image.get_rect()
		
		self.pos = vector.Vector2D(position[0], position[1])
		self.vel = vector.Vector2D(velocity[0], velocity[1])
		
#		config.sounds['ball.wav'].play()

		self.lastTime = 0
		
	def bounceX(self):
		self.vel.x *= -1
		
	def bounceY(self):
		self.vel.y *= -1

	def border_collision(self, pos, arena):
		""" Left and right boundaries of play area	"""
		if pos.x < arena.x or pos.x > arena.x + arena.w-size:
			if pos.x < arena.x:
				pos.x = arena.x
			if pos.x > arena.x + arena.w-size:
				pos.x = arena.x + arena.w-size
			self.bounceX()
		""" Upper boundary of play area """
		if pos.y < arena.y:
			pos.y = arena.y
			self.bounceY()
		""" Lower boundary of play area	"""
		if pos.y > arena.y + arena.h - size:
			pos.y = arena.y + arena.h - size
			if config.demo:
				self.bounceY()
			else:
				self.kill()
				config.sounds['pit.wav'].play()
		self.pos = pos
		return self.pos
	
	def ball_collision(self, ball):
		pass

	def update(self, time):
		
		nextpos = self.pos + (self.vel * time)
		
		self.lastTime += time
		
		if self.lastTime > Ball.ttn:
			self.image = self.animation[self.animation.currentFrame()]
			self.animation.nextFrame()
			self.lastTime %= Ball.ttn

		nextpos = self.border_collision(nextpos, config.play_size)
		
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
