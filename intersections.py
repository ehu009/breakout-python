
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

