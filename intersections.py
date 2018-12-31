
from math import sqrt

from vector import Vector2D

			
def intersect_circle_circle(a_pos, a_radius, b_pos, b_radius):
	""" a_pos and b_pos are both vectors
	and	b_radius and a_radius are decimal numbers"""
		
	#vector from A to B
	
	difference = b_pos - a_pos
	distance = difference.magnitude()
	
	if a_radius + b_radius >= distance:
		return True
	else:
		return False



def intersect_circle_rectangle(a_pos, a_radius, b_pos, b_size):
	""" A is a circle
		B is a rectangle defined by two vectors"""
	
	# position of rectangles walls relative to circle center
	
	top = b_pos.y - a_pos.y
	bottom = (b_pos.y + b_size.y) - a_pos.y
	
	left = b_pos.x - a_pos.x
	right = (b_pos.x + b_size.x) - a_pos.x
	
	
	#is the ball too close?
	intersecting = (left <= a_radius) and (top <= a_radius) and (right >= -a_radius) and (bottom >= -a_radius)
	
	
	if intersecting:
		return True
	else:
		return False



def ft(x):	
	if x == 0:
		return 0
	return x/abs(x)
# Hit-test: Rect, Ball
def intersection_BR (ball, r):		
	#	Input:	| - ball: Ball object
	#			| - rect: Rect object
	#		ball and rect objects have (x,y) coordinates i in top-left corner
	#	Return:	| - If Ball og Rect har kollidert:
	#			|  	Vector2D object indicating surface on Rect hit by Ball
	#			| - Ellers: False
	#
	rad = ball.radius	#Radius
	hw = r.rect.w/2		#Distance from centre of Rect to left/right edges/corners
	hh = r.rect.h/2		#Distance from centre of Rect to top/bottom edges/corners
	
	dx = (ball.pos.x+rad)-(r.rect.x+hw)	#Ball x-position relative to Rect
	dy = (ball.pos.y+rad)-(r.rect.y+hh)	#Ball y-position relative to Rect
	dist = sqrt(dx**2 + dy**2)	#Actual distance between centres
	
	mDX = rad + hw					#Maximum dx
	mDY = rad + hh					#Maximum dy
	maxD= sqrt(mDX**2+mDY**2)	#Maximum distance between centres
	#make x, y distances into ratios
	dx /= mDX 
	dy /= mDY
	#return false if Rect and Ball are not close enough
	if dist > maxD or abs(dx) > 1 or abs(dy) > 1:
		return False
	
	#make variables representing a surface on a square/rectangle
	
	return True











class Circle():

	def __init__(self, radius, position=None):
		self.radius = radius
		if position is not None:
			self.pos = position



class RoundCollider():

	def __init__(self, position=None, radius = None, velocity=None):
		
		if position is not None:
			self.pos = position
		if radius is not None:
			self.radius = radius
		if velocity is not None:
			self.vel = velocity
	#	super(RoundCollider, self).__init__(position, velocity)

		self._colliderect = None
	
	def bounceX(self):
		self.vel.x *= -1

	def bounceY(self):
		self.vel.y *= -1

	def _rect_colliderect(self, r):
		top	= (r.y ) - self.pos.y
		bottom = (r.y + r.h) - self.pos.y 
		left   = (r.x ) - self.pos.x
		right  = (r.x + r.w) - self.pos.x

		if left <= self.radius and top <= self.radius and right >= -self.radius and bottom >= -self.radius:
			self._colliderect = pygame.Rect(left, right, top, bottom)

	def _bounce_circle_off_box(self):
		#assumes c has radius and vector position
		#assumes b has vector position and int sizes
		
		if self._colliderect is None:
			return
		
		if abs(self._colliderect.x) < self.r and self.vel.x > 0:
			self.bounceX()
		if abs(self._colliderect.w) < self.r and self.vel.x < 0:
			self.bounceX()
		if abs(self._colliderect.h) < self.r and self.vel.y > 0:
			self.bounceY()
		if abs(self._colliderect.y) < self.r and self.vel.y < 0:
			self.bounceY()

	def rect_collision (self, rect):
		self._colliderect = None
		self._rect_colliderect(rect)
		self._bounce_circle_off_box(rect)
		return (self._colliderect is not None)


"""

"""





