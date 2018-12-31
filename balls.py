import pygame

import config
import vector
import animate

import intersections

group = pygame.sprite.Group()


size = config.ball_size
arena = config.play_size


class Circle():

	def __init__(self, radius, position=None):
		self.radius = radius
		if position is not None:
			self.pos = position

class Ball (pygame.sprite.Sprite, Circle):
	
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

		self.radius = 24/2

		
		
		self.animation = Ball.animation

		self.image = self.animation[0]
		self.rect = self.image.get_rect()
		
		self.pos = vector.Vector2D(position[0], position[1])
		self.vel = vector.Vector2D(velocity[0], velocity[1])
		
		super(Ball, self).__init__()
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
		return pos
	
	def _rect_collision(self,  rect):
		# Compare with zero
		def ft(x):	
			if x == 0:
				return 0
			return x/abs(x)
		# Hit-test: Rect, Ball
		def intersection_vector (ball, rect):		
			#	Input:	| - ball: Ball object
			#			| - rect: Rect object
			#		ball and rect objects have (x,y) coordinates i in top-left corner
			#	Return:	| - If Ball og Rect har kollidert:
			#			|  	Vector2D object indicating surface on Rect hit by Ball
			#			| - Ellers: False
			#
			rad = ball.radius	#Radius
			hw = rect.w/2		#Distance from centre of Rect to left/right edges/corners
			hh = rect.h/2		#Distance from centre of Rect to top/bottom edges/corners
			
			dx = (ball.pos.x+rad)-(rect.x+hw)	#Ball x-position relative to Rect
			dy = (ball.pos.y+rad)-(rect.y+hh)	#Ball y-position relative to Rect
			
			mDX = rad + hw					#Maximum dx
			mDY = rad + hh					#Maximum dy
			#make x, y distances into ratios
			dx /= mDX 
			dy /= mDY
			
			#make variables representing a surface on a square/rectangle
			xdir = 0
			ydir = 0
			v = vector.Vector2D(0,0)
			if abs(dx) == abs(dy):
				if abs(dx) == 0:				#centre
					return v
				v.x = ft(dx)
				v.y = ft(dy)
				return v #corners
			if abs(dx) > abs(dy):	#left/right sides
				xdir = ft(dx)
				ydir = 0
			elif abs(dy) > abs(dx):	#top/bottom sides
				xdir = 0
				ydir = ft(dy)
			v.x = xdir
			v.y = ydir
			return v
		
		v = intersection_vector(self, rect)
		print v
		if abs(v.x) == abs(v.y): 	#for corners
			if ft(self.vel.y) == v.y*-1:
				self.bounceX()
			if ft(self.vel.x) == v.x*-1:
				self.bounceY()
		else:				
			
							#for sides
			if v.x != 0:
				self.bounceX()
				
			if v.y != 0:
				
				self.bounceY()
			
		#reposition ball
		hw = rect.w/2
		hh = rect.h/2
		rad = self.radius
		if v.x < 0:
			self.pos.x = v.x *(hw + rad*2 + 1) +(rect.x + hw)
		if v.x > 0:
			self.pos.x = v.x *(hw + 1) +(rect.x + hw)
		if v.y < 0:
			self.pos.y = v.y *(hh + rad*2 +1) +(rect.y + hh)
		if v.y > 0:
			self.pos.y = v.y *(hh + 1) +(rect.y + hh)
		return True

		
		
	def update(self, time, blocks):
		
		nextpos = self.pos + (self.vel * time)
		
		self.lastTime += time
		
		if self.lastTime > Ball.ttn:
			self.image = self.animation[self.animation.currentFrame()]
			self.animation.nextFrame()
			self.lastTime %= Ball.ttn

		""" interact with walls """
		nextpos = self.border_collision(nextpos, config.play_size)
		self.pos = nextpos

		""" interact with blocks """
		blocks = pygame.sprite.spritecollide(self, blocks, True, intersections.intersection_BR)
		for block in blocks:
			self._rect_collision(block.rect)

		


		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
