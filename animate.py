import pygame


class Sequenced(list):

	def __init__ (self, source, frames):
		
		super(Sequenced, self).__init__()

		for tupl in frames:
			img = source.subsurface(tupl)
			self.append(img)

		self.cFrame = 0

	def currentFrame(self):
		return self.cFrame

	def nextFrame(self):
		self.cFrame = (self.cFrame + 1) % (len(self))
		
	def prevFrame(self):
		if self.cFrame == 0:
			self.cFrame = len(self.frames) - 1
		else:
			self.cFrame -= 1