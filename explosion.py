import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Explosion(Sprite):
	"""A class to manage bullets fired from the player."""

	def __init__(self, game):
		super().__init__()
		"""Create a explosion object at the enemy last position."""
		self.screen = game.screen
		self.settings = game.settings

		# Load image, get rect and place on top of player
		self.image = pygame.image.load('sprites/enemy_explosion1.bmp')
		self.rect = self.image.get_rect()

		# List of all sprites for an animated sprite
		self.sprite_list = [pygame.image.load('sprites/explosion1.bmp'),
							pygame.image.load('sprites/explosion2.bmp'),
							pygame.image.load('sprites/explosion3.bmp'),
							pygame.image.load('sprites/explosion4.bmp')]

		# Will be used for changing images and animate the sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 100
		self.is_active = True

		# Store the explosion position as a decimal value.
		self.y = float(self.rect.y)

	def get_position(self, position1, position2):
		"""Set the rect according to values passed by main.py"""
		self.rect.centerx = position1
		self.rect.centery = position2

	def check_state(self):
		"""Return true or false depending on self.is_active"""
		return self.is_active



	def update(self):
		"""Animate the sprite."""

		if self.is_active:

			if pygame.time.get_ticks() - self.last_update > self.image_interval:
				self.image_value += 1
				self.last_update = pygame.time.get_ticks()

			if self.image_value >= len(self.sprite_list):
				self.is_active = False
				self.image_value = 0
		
		self.image = self.sprite_list[self.image_value]


	def draw(self):
		"""Draw the explosion into the screen."""
		self.screen.blit(self.image, self.rect)