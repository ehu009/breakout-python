
import os
import sys
import math
import random

import pygame
#import pygame.image

import keyboard
import intersections
import vector
import animate
##################



demo = False


#	prefer window in top-right corner
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1080,0)


"""
let's assume we have a left and right border
	having THICCNESS divisible by 8"""
"""
main play field should be
	uuuh 5:3 perhaps?
	"""

sprite_size = 8
ball_size = 24

play_area_ratio = (5, 3)
play_area_scale = 12


border_thickness = 8

play_size = pygame.Rect(0, 0, play_area_ratio[0]*sprite_size*play_area_scale, play_area_ratio[1]*sprite_size*play_area_scale)
border_size = (sprite_size * border_thickness, play_size.h)


play_size.x = border_size[0]
screen_size = (play_size.w + 2*border_size[0], play_size.h)





image_paths = (os.path.join("img", "tileset.png"), os.path.join("img", "player.png"), os.path.join("img", "ball.png"))

tileset_image = pygame.image.load(image_paths[0])
racket_image = pygame.image.load(image_paths[1])
ball_image = pygame.image.load(image_paths[2])



class Paddle (pygame.sprite.Sprite):

	def __init__(self):
		super(Paddle, self).__init__()
		y = play_size.h -3*sprite_size
		x = play_size.x

		self.pos = vector.Vector2D(x, y)
		self.vel = vector.Vector2D(0, 0)
		self.rect = pygame.Rect(x, y, 6*sprite_size, 2*sprite_size)
		self.image = racket_image

	def draw(self, screen):
		screen.blit(self.image, self.rect)
	

	def update(self, time, x_input):
		def_speed = 0.3

		self.vel.x = 0
		if self.pos.x > play_size.x:
			if x_input < 0:
				""" move to the left """
				self.vel.x = -def_speed
		if self.pos.x < play_size.x + play_size.w - sprite_size*6:
			if x_input > 0:
				""" move to the right """
				self.vel.x = def_speed
		
		self.pos.x += self.vel.x*time

		self.rect.x = self.pos.x


class Graphic (pygame.sprite.Sprite):
	
	def __init__(self, position, frame=-1):
		super(Graphic, self).__init__()
		
		r = pygame.Rect(0, 0, sprite_size, sprite_size)
		x = frame
		if x == -1:
			x = random.randint(0, 5)
		
		r.x = x * sprite_size


		self.image = tileset_image.subsurface(r)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]



class Block (pygame.sprite.Sprite):
	
	def __init__(self, position, frame=-1):
		super(Block, self).__init__()
		
		r = pygame.Rect(0, 0, sprite_size, sprite_size)
		x = frame
		if x == -1:
			x = random.randint(0,6)
		r.x = x * 8
		self.image = tileset_image.subsurface(r)
		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]
		



ball_animation = list()
for x in range (0,4):
	ball_animation.append((ball_size*x,0, ball_size, ball_size))
		
seq1 = animate.Sequenced(ball_image, ball_animation)	



class Ball (pygame.sprite.Sprite):
	
	group = pygame.sprite.Group()
	
	ttn = 40

	def __init__(self, position, velocity):
		
		super(Ball, self).__init__()
		
		self.animation = seq1

		self.image = self.animation[0]
		self.rect = self.image.get_rect()
		
		self.pos = vector.Vector2D(position[0], position[1])
		self.vel = vector.Vector2D(velocity[0], velocity[1])
		
		self.lastTime = 0
		
	def bounceX(self):
		self.vel.x *= -1
		
	def bounceY(self):
		self.vel.y *= -1

	def update(self, time):
		
		nextpos = self.pos + (self.vel * time)
		
		self.lastTime += time
		
		if self.lastTime > Ball.ttn:
				
			self.image = self.animation[self.animation.currentFrame()]
			self.animation.nextFrame()
			self.lastTime %= Ball.ttn

		""" Left and right boundaries of play area	"""
		if nextpos.x < play_size.x or nextpos.x > play_size.x + play_size.w-24:
			if nextpos.x < play_size.x:
				nextpos.x = play_size.x
			if nextpos.x > play_size.x + play_size.w-24:
				nextpos.x = play_size.x + play_size.w-24
			self.bounceX()
		""" Upper boundary of play area """
		if nextpos.y < play_size.y:
			if nextpos.y < play_size.y:
				nextpos.y = play_size.y
			self.bounceY()
		
		""" Lower boundary of play area	"""
		if nextpos.y > play_size.y + play_size.h - 24:
			nextpos.y = play_size.y + play_size.h - 24
			if demo:
				self.bounceY()
			else:
				self.kill()
		
		
		self.pos = nextpos
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		

graphic_group = pygame.sprite.Group()

ball_group = pygame.sprite.Group()

def border_graphics (g):
	for y in range (0,border_size[1]/8):
		for x in range (0, border_size[0]/8):
			blk = Graphic((x*8, y*8))
			g.add(blk)
		
	for y in range (0,border_size[1]/8):
		for x in range (0, border_size[0]/8):
			blk = Graphic((x*8 + (screen_size[0] - border_size[0]), y*8))
			g.add(blk)


	
block_group = pygame.sprite.Group()			



def randomBalls(g):

	for x in range(0, random.randint(3,7)):
		pos_y = random.randint(0, play_size.h - ball_size)
		pos_x = random.randint(play_size.x, play_size.x + play_size.w - 24)
		pos = (pos_x, pos_y)

		vel_x = float(random.randint(10,20))
		vel_y = float(random.randint(10,20))
		
		vel_x /=83
		vel_y /=83
		vel = (vel_x, vel_y)

		b = Ball(pos, vel)
		b.add(g)

class GameDemo(object):

	def __init__(self):
		self.ended = False
		self.paused = False

		self.keys = keyboard.Listener()
		
		border_graphics(graphic_group)

		randomBalls(ball_group)
	
		
	def update(self, time):
		self.keys.update()
		if self.paused:
			if self.keys[keyboard.M.SPC]:
				self.paused = False
		else:
			if self.keys[keyboard.M.SPC]:
				self.paused = True






			ball_group.update(time)




		if self.keys[keyboard.M.ESC]:
			self.end()
		
		return self.ended

	def draw(self, screen):			
		
		screen.fill((0,0,0))
		
		ball_group.draw(screen)
		graphic_group.draw(screen)
		
	def end(self):
		self.ended = True



class Game(object):
	
	
	def __init__(self):
		self.ended = False
		self.paused = False
		self.keys = keyboard.Listener()

		self.player = Paddle()

		border_graphics(graphic_group)

		num_blocks_x = (play_size.w - 2*sprite_size) / sprite_size
		for y in range(0, 3):
			y_coord = sprite_size * (y + 1)
			for x in range(0,num_blocks_x):
				x_coord = (1+x)*sprite_size + play_size.x
				b = Block( ( x_coord, y_coord),y%6)
				b.add(block_group)



	
	def draw(self, screen):

		screen.fill((0,0,0))
		
		graphic_group.draw(screen)

		block_group.draw(screen)

		ball_group.draw(screen)


		self.player.draw(screen)


	def update(self, time):
		
		self.keys.update()
		if self.paused:
			if self.keys[keyboard.M.SPC]:
				self.paused = False
		else:
			if self.keys[keyboard.M.SPC]:
				self.paused = True

			x_dir = self.keys[keyboard.M.RGT]
			x_dir -= self.keys[keyboard.M.LFT]
			self.player.update(time, x_dir)


		if self.keys[keyboard.M.ESC]:
			self.end()
		
		return self.ended
		
	def end(self):
		self.ended = True








if __name__ == "__main__":
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "-d" or sys.argv[1] == "--demo":
			demo = True



	pygame.init()
	
	screen = pygame.display.set_mode(screen_size)
	
	
	
	game = None
	if demo:
		game = GameDemo()
	else:
		game = Game()



	
	time = 10
	
	while(1):
		time_spent = - pygame.time.get_ticks()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				game.end()
		
		if game.update(time):
			break
		
		if not game.paused:
			
			game.draw(screen)
			pygame.display.flip()
		


		time_spent += pygame.time.get_ticks()
		time = time_spent
		


		pygame.time.delay(5)
		
	pygame.quit()
	
