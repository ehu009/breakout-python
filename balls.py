import math

import pygame

import config
import vector
import animate

import intersections

import blocks


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
		print "ball bounced horizontally"
		
	def bounceY(self):
		self.vel.y *= -1
		print "ball bounced vertically"

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
	
	@staticmethod
	def _bounce (p, radius, r):
		half = (float(r.w)/2, float(r.h)/2)
		center = (p.x + radius - (r.x+half[0]), p.y + radius - (r.y+half[1]))
		side = (abs(center[0]) - half[0], abs(center[1]) - half[1])

		if (side[0] > radius or side[1] > radius):
			return False
		if (side[0] < -radius and side[1] < -radius):
			return False

		if (side[0] < 0 or side[1] < 0):
			dx = 0
			dy = 0
			if (abs(side[0]) < radius and side[1] < 0):
				if center[0]*side[0] < 0:
					dx = -1
				else:
					dx = 1
			elif (abs(side[1]) < radius and side[0] < 0):
				if (center[1]*side[1] < 0):
					dy = -1
				else:
					dy = 1
			return (dx, dy)
		bounce = (side[0] ** 2) + (side[1] ** 2) < radius ** 2
		if (bounce is False):
			return False
		norm = math.sqrt((side[0] ** 2) + (side[1] ** 2))
		dx = float(1)
		if center[0] < 0:
			dx = -1
		dy = float(1)
		if center[1] < 1:
			dy = -1
		dx *= side[0]
		dx /= norm
		dy *= side[1]
		dy /= norm
		return (dx, dy, norm)


	def update(self, time, blocks):

		nextpos = self.pos + (self.vel * time)
		
		self.lastTime += time
		
		if self.lastTime > Ball.ttn:
			self.image = self.animation[self.animation.currentFrame()]
			self.animation.nextFrame()
			self.lastTime %= Ball.ttn

		""" interact with walls """
		nextpos = self.border_collision(nextpos, config.play_size)
		

		""" interact with blocks """
		bounced = False
		speed = self.vel.magnitude()
		for block in blocks:
			v = Ball._bounce(nextpos, self.radius, block.rect)
			if v is not False and v != (0, 0):
				bounced = True
				
				# adjust velocity
				vec = vector.Vector2D(v[0], v[1])
				vec *= speed
				self.vel = vec
				
				# add code here for what happens to the blocks
				# ...
		if bounced:
			# sounds, animations or something
			pass	
				

		self.pos = nextpos		
		
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y


import keyboard






if __name__ == "__main__":
	pygame.init()
	pygame.mixer.init()


	block_x = 400
	block_y = 100

	b = blocks.Block((block_x, block_y))
	blocks.group.add(b)

	spawn_x = block_x -200
	spawn_y = 100-24


	def spawn(x, y):
		b_pos = (x, y)

		vx = 4
		vy = 0

		b = Ball(b_pos, (vx, vy))
		group.add(b)

	screen = pygame.display.set_mode(config.screen_size)
	
	key = keyboard.Listener()
	""" no menu or anything yet """
	
	quit = False

	spawned = False

	time = 10
	while(not quit):
		time_spent = - pygame.time.get_ticks()
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				quit = True
		
		if (key[keyboard.M.ESC]):
			quit = True
		if (key[keyboard.M.SPC] and not spawned):
			spawn(spawn_x, spawn_y)
			spawn_y += 2
			spawned = True
		elif spawned == True and key[keyboard.M.SPC] == 0:
			spawned = False

		screen.fill(0)
		key.update()
		group.update(time, blocks.group)
		group.draw(screen)
		blocks.group.draw(screen)

		pygame.display.flip()

		time_spent += pygame.time.get_ticks()
		time = time_spent
		
		pygame.time.delay(5)
		
	pygame.quit()
	print "Good-bye~"
