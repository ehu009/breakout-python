
import os
import sys
import math
import random

import pygame

import keyboard
import intersections
import vector
import animate
from staticgfx import *
import config
import balls
from paddle import Paddle
from scores import Scoreboard

##################


def border_graphics (g):
	bs = config.border_size
	zs = config.sprite_size
	for y in range (0,bs[1]/zs):
		for x in range (0, bs[0]/zs):
			blk = Graphic((x*zs, y*zs))
			g.add(blk)
		
	for y in range (0,bs[1]/zs):
		for x in range (0, bs[0]/zs):
			blk = Graphic((x*zs + (config.screen_size[0] - bs[0]), y*zs))
			g.add(blk)




class Block (pygame.sprite.Sprite):
	
	def __init__(self, position, frame=-1):
		
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
		super(Block, self).__init__()






	

block_group = pygame.sprite.Group()			



def demo_blocks(g):
	ss = config.sprite_size
	ps = config.play_size
	num_blocks_x = (ps.w - 2*ss) / ss
	for y in range(0, 3):
		y_coord = ss * (y + 1)
		for x in range(0,num_blocks_x):
			x_coord = (1+x)*ss + ps.x
			b = Block( ( x_coord, y_coord),y%6)
			g.add(b)

def demo_balls(g):
	ps = config.play_size
	for x in range(0, random.randint(3,7)):
		pos_y = random.randint(1, ps.h - 1 - config.ball_size)
		pos_x = random.randint(ps.x + 1, ps.x - 1 + ps.w - 24)
		pos = (pos_x, pos_y)

		vel_x = float(random.randint(10, 20))
		vel_y = float(random.randint(10, 20))
		
		vel_x /= 83
		vel_y /= 83
		vel = (vel_x, vel_y)

		b = balls.Ball(pos, vel)
		b.add(g)


class GameDemo(object):

	def __init__(self):
		self.ended = False
		self.paused = False

		self.keys = keyboard.Listener()
		
		border_graphics(graphic_group)

		demo_balls(balls.group)

		self.ttnBlock = 130
		
	def update(self, time):
		self.keys.update()
		if self.paused:
			if self.keys[keyboard.M.SPC]:
				self.paused = False
		else:
			if self.keys[keyboard.M.SPC]:
				self.paused = True


			balls.group.update(time)
		
		#spawn a block somewhere
		if self.ttnBlock <= 0:
			ps = config.play_size
			x = ps.w / config.sprite_size
			x = random.randint(0, x)
			x *= config.sprite_size
			x += ps.x

			y = ps.h / config.sprite_size
			y = random.randint(0, y)
			y *= config.sprite_size
			y += ps.y

			block_group.add(Block((x,y)))

			self.ttnBlock = 130


		if self.keys[keyboard.M.ESC]:
			self.end()
		return self.ended

	def draw(self, screen):
		screen.fill((0,0,0))
		
		balls.group.draw(screen)
		graphic_group.draw(screen)
		
	def end(self):
		self.ended = True



from intersections import intersection_BR

class Game(object):
	
	
	def __init__(self):
		self.ended = False
		self.paused = False
		self.keys = keyboard.Listener()

		self.player = Paddle()
		self.scores = Scoreboard((0,20*config.sprite_size), 57)
		
		border_graphics(graphic_group)
		demo_blocks(block_group)


	def draw(self, screen):
		screen.fill((0,0,0))
		
		graphic_group.draw(screen)
		block_group.draw(screen)
		balls.group.draw(screen)

		self.scores.draw(screen)
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
			self.player.update(time, x_dir, self.keys[keyboard.M.UP]-0)
			
				
			balls.group.update(time, block_group)

			
			"""
			for key, value in block_collisions.iteritems():
				if value == None:
					continue
				for block in value:
					# determine if ball bounces off vertically or horizontally
					d = vector.Vector2D(key.pos.x, key.pos.y)
					
					d.x -= block.rect.x
					d.y -= block.rect.y

					if d.x ** 2 < d.y ** 2:
						key.bounceX()
					else:
						key.bounceY()
					#	destroy block 
					del block
				config.sounds['beep.wav'].play()
			"""


			# update balls
			# update blocks
			self.scores.update()

		if self.keys[keyboard.M.ESC]:
			self.end()
		
		return self.ended
		
	def end(self):
		self.ended = True




def start_menu():
	pass

if __name__ == "__main__":
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "-d" or sys.argv[1] == "--demo":
			config.demo = True
			#	prefer window in top-right corner
			os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (945,18)
	
	pygame.init()
	pygame.mixer.init()

	config.load_sounds()	

	screen = pygame.display.set_mode(config.screen_size)
	
	
	""" no menu or anything yet """
	start_menu()

	game = None
	if config.demo:
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
	print "Good-bye~"
