#!/usr/bin/env Python

import pygame
from pygame.locals import *


class M:
	"""Keyboard Macros"""
	ESC, UP, RGT, LFT, SPC = range(5)
	
class Listener(list):
	"""Listens to keystrokes"""
	def __init__(self):
		
		super(Listener, self).__init__()
		
		for i in range(5):
			self.append(0)
		
	def update (self):
		
		e = pygame.key.get_pressed()
		
		""" translate keys """
		if e[K_LEFT] ^ e[K_RIGHT]:
			self[M.LFT] = bool(e[K_LEFT])
			self[M.RGT] = bool(e[K_RIGHT])
			
		elif not (e[K_LEFT] or e[K_RIGHT]):
			self[M.LFT] = False
			self[M.RGT] = False
		
		self[M.SPC] = bool(e[K_SPACE])

		self[M.UP] = bool(e[K_UP])
		self[M.ESC] = bool(e[K_ESCAPE])
		
	def __repr__(self):
		print "state of our keyboard: "
		s = ""
		for k in range(4):
			s += repr(self[k]) + " "
		return s
