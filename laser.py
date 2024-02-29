import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Laser(Sprite):
	"""A class to manage laser powerup."""

	def __init__(self, game):
		super().__init__()
		"""Create a bullet object at the player current position."""
		self.screen = game.screen
		self.settings = game.settings
		self.game = game
		self.player = game.player

		# Load image, get rect and place on top of player
		self.image = pygame.image.load('sprites/laser1.bmp')
		self.rect = self.image.get_rect()
		self.rect.midbottom = self.player.rect.midtop

		# List of all sprites for an animated sprite
		self.sprite_list = [pygame.image.load('sprites/laser1.bmp'),
							pygame.image.load('sprites/laser2.bmp'),
							pygame.image.load('sprites/laser3.bmp'),
							pygame.image.load('sprites/laser4.bmp'),
							pygame.image.load('sprites/laser5.bmp'),
							pygame.image.load('sprites/laser6.bmp'),
							pygame.image.load('sprites/laser7.bmp'),
							pygame.image.load('sprites/laser8.bmp')]

		# Will be used for changing images and animate the sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 100

		self.timer = 10000
		
		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)


	def update(self):
		"""Moves the bullet up and animated the sprite."""
		# Update the decimal value of the bullet
		self.x = self.player.rect.centerx
		self.y = self.player.rect.midtop
		# Update the rect position
		self.rect.centerx =  self.x
		self.rect.midbottom = self.y 


		if pygame.time.get_ticks() - self.last_update > self.image_interval:
			self.image_value += 1
			self.last_update = pygame.time.get_ticks()

		if self.image_value >= len(self.sprite_list):
			self.image_value = 0
		
		self.image = self.sprite_list[self.image_value]


	def draw_laser(self):
		"""Draw the bullet into the screen."""
		self.screen.blit(self.image, self.rect)


class Beam(Laser):
	"""This class will be used to create a beam to check when the player is directly under an alien
		it will inherit from the Laser class because it will work the same way as the Laser"""
	def __init__(self, game):
		super().__init__(game)
		"""Load the image and get rect, this image is transparent so the player won't see it"""
		self.image = pygame.image.load('sprites/checker_beam.bmp')
		self.rect = self.image.get_rect()


	def update(self):
		"""It will update the same way Laser does, so just inherit it."""
		self.x = self.player.rect.centerx
		self.y = self.player.rect.midtop
		# Update the rect position
		self.rect.centerx =  self.x
		self.rect.midbottom = self.y 

	def draw_beam(self):
		"""Draw the beam into the screen."""
		self.screen.blit(self.image, self.rect)