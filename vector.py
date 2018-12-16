import math

class Vector2D(object):
	"""implements a vector in 2D"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __add__(self, b):
		return Vector2D(self.x + b.x, self.y + b.y)
	
	def __sub__(self, b):
		return Vector2D(self.x - b.x, self.y - b.y)
	
	def __repr__(self):
		return "Vector(%s, %s)" % (self.x, self.y)
		
	def __mul__(self, b):
		"""assuming B is a scalar"""
		try:
			b = float(b)
			return Vector2D(self.x*b, self.y*b)
		except ValueError:
			print "right hand side must be a float (decimal number)"
			raise
	
	def magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
			
	def normalize(self):
		"""return a vector with magnitude = 1"""
		
		try:
			m = self.magnitude()
			return Vector2D(self.x / m, self.y / m)
		except ZeroDivisionError:
			print "whoops, i tried to divide by zero, but i am a computer"
			raise
			
	def copy(self):
		return Vector2D(self.x, self.y)
		
			
		
	
		
		
		
		
		
		
		
		
