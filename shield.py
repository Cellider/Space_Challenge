import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Shield(Sprite):
	"""A class to manage player's shield."""

	def __init__(self, game):
		super().__init__()
		"""Create a shield object at the player current position."""
		self.screen = game.screen
		self.settings = game.settings
		self.game = game
		self.player = game.player

		# Load image, get rect and place inside of the player rect
		self.main_image = pygame.image.load('sprites/shield1.bmp')
		self.image = self.main_image
		self.rect = self.main_image.get_rect()
		self.rect.center = self.player.rect.center

		# List of all sprites for an animated sprite
		self.sprite_list = [pygame.image.load('sprites/shield1.bmp'),
							pygame.image.load('sprites/shield2.bmp'),
							pygame.image.load('sprites/shield3.bmp'),
							pygame.image.load('sprites/shield4.bmp'),
							pygame.image.load('sprites/shield5.bmp'),
							pygame.image.load('sprites/shield6.bmp'),
							pygame.image.load('sprites/shield7.bmp'),
							pygame.image.load('sprites/shield8.bmp'),
							pygame.image.load('sprites/shield9.bmp'),
							pygame.image.load('sprites/shield10.bmp'),
							pygame.image.load('sprites/shield11.bmp'),
							pygame.image.load('sprites/shield12.bmp'),
							pygame.image.load('sprites/shield13.bmp'),
							pygame.image.load('sprites/shield14.bmp'),
							pygame.image.load('sprites/shield15.bmp'),
							pygame.image.load('sprites/shield16.bmp'),
							pygame.image.load('sprites/shield17.bmp'),
							pygame.image.load('sprites/shield18.bmp'),
							pygame.image.load('sprites/shield19.bmp'),
							pygame.image.load('sprites/shield20.bmp'),
							pygame.image.load('sprites/shield21.bmp'),
							pygame.image.load('sprites/shield22.bmp'),
							pygame.image.load('sprites/shield23.bmp'),
							pygame.image.load('sprites/shield24.bmp'),
							pygame.image.load('sprites/shield25.bmp'),
							pygame.image.load('sprites/shield26.bmp'),
							pygame.image.load('sprites/shield27.bmp'),
							pygame.image.load('sprites/shield28.bmp'),
							pygame.image.load('sprites/shield29.bmp'),
							pygame.image.load('sprites/shield30.bmp'),
							pygame.image.load('sprites/shield31.bmp')]

		# Keep track of the shield current state
		self.active = False
		self.turn_shield_on = False

		# Will be used for changing images and animate the sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 100
		
		# Store the canon position as a decimal value.
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)

	def activate(self):
		"""Activate the shield animation."""
		self.active = True
		self.turn_shield_on = True

	def deactivate(self):
		"""Activate the shield animation backwards."""
		self.turn_shield_on = False

	def shield_state(self):
		"""Return true or false depending on self.active"""
		if self.active == True:
			return True
		elif self.active == False:
			return False

	def update(self):
		"""Moves gun sprite according to player movement"""
		# Update the decimal value of the gun
		self.x = self.player.rect.centerx
		self.y = self.player.rect.centery
		# Update the rect position
		self.rect.centerx =  self.x
		self.rect.centery = self.y

		if self.active:

			if pygame.time.get_ticks() - self.last_update > self.image_interval and self.turn_shield_on:
				# Stop looping through the animation once it has reach the end
				if self.image_value < 30:
					self.image_value += 1
					self.last_update = pygame.time.get_ticks()

			elif pygame.time.get_ticks() - self.last_update > self.image_interval and not self.turn_shield_on:
				# Once the shield is set to turn off, we simply go through the load animation backwards
				self.image_value -= 1
				self.last_update = pygame.time.get_ticks()
				# Will stop the loop once the animation has ended
				if self.image_value == 0:
					self.active = False

			self.image = self.sprite_list[self.image_value]

		## if no animation is playing, simply use the default image
		if not self.active:
			self.image = self.main_image

	def draw(self):
		"""Draw the gun into the screen."""
		self.screen.blit(self.image, self.rect)
