
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
