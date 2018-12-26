#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import pygame

import config


class Text(pygame.sprite.Sprite):


	lookup = None
	@staticmethod
	def __load_images(size):
		""" size = width of sprites """
		
		l = dict()
		sprites = list()
		
		keys = ("<", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', '@')
		for y in range(1, 4):
			for x in range(0,10):
				sprites.append(pygame.Rect(x*size, y*size, size, size))
		for c in range(0,len(keys)-1):
			key = keys[c]
			value = config.tileset_image.subsurface(sprites[c])
			l[key] = value
		Text.lookup = l

	def __init__(self, position=(80,80), value="testus"):
		ss = config.sprite_size
		if Text.lookup == None:
			Text.__load_images(ss)
		
		self.value = value
		super(Text, self).__init__()
		size = (len(value)*ss, ss)
		self.image = pygame.Surface(size)

		self.rect = self.image.get_rect()
		self.rect.x = position[0]
		self.rect.y = position[1]

	def update(self):
		pass

	def draw(self, screen):
		r = pygame.Rect(0, 0, config.sprite_size, config.sprite_size)
		for letter in self.value:
			self.image.blit(Text.lookup[letter], r)
			r.x += config.sprite_size
		screen.blit(self.image, self.rect)

