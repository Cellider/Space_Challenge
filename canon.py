import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Canon(Sprite):
	"""A class to manage player's canon sprite so that animations can work separately"""

	def __init__(self, game):
		super().__init__()
		"""Create a canon object at the player current position."""
		self.screen = game.screen
		self.settings = game.settings
		self.game = game
		self.player = game.player

		# Load image, get rect and place inside of the player rect
		self.main_image = pygame.image.load('sprites/canon.bmp')
		self.image = self.main_image
		self.rect = self.main_image.get_rect()
		self.rect.center = self.player.rect.center

		# List of all sprites for an animated sprite
		self.loading_canon = [pygame.image.load('sprites/canon1.bmp'),
							pygame.image.load('sprites/canon2.bmp'),
							pygame.image.load('sprites/canon3.bmp'),
							pygame.image.load('sprites/canon4.bmp'),
							pygame.image.load('sprites/canon5.bmp'),
							pygame.image.load('sprites/canon6.bmp'),
							pygame.image.load('sprites/canon7.bmp'),
							pygame.image.load('sprites/canon8.bmp'),
							pygame.image.load('sprites/canon9.bmp'),
							pygame.image.load('sprites/canon10.bmp'),
							pygame.image.load('sprites/canon11.bmp'),
							pygame.image.load('sprites/canon12.bmp'),
							pygame.image.load('sprites/canon13.bmp'),
							pygame.image.load('sprites/canon14.bmp'),
							pygame.image.load('sprites/canon15.bmp'),
							pygame.image.load('sprites/canon16.bmp'),
							pygame.image.load('sprites/canon17.bmp'),
							pygame.image.load('sprites/canon18.bmp'),
							pygame.image.load('sprites/canon19.bmp'),
							pygame.image.load('sprites/canon20.bmp'),
							pygame.image.load('sprites/canon21.bmp'),
							pygame.image.load('sprites/canon22.bmp'),
							pygame.image.load('sprites/canon23.bmp'),
							pygame.image.load('sprites/canon24.bmp'),
							pygame.image.load('sprites/canon25.bmp'),
							pygame.image.load('sprites/canon26.bmp'),
							pygame.image.load('sprites/canon27.bmp'),
							pygame.image.load('sprites/canon28.bmp'),
							pygame.image.load('sprites/canon29.bmp')]
		
		self.fire_laser = [	pygame.image.load('sprites/canon30.bmp'),
						pygame.image.load('sprites/canon31.bmp'),
						pygame.image.load('sprites/canon32.bmp'),
						pygame.image.load('sprites/canon33.bmp'),
						pygame.image.load('sprites/canon34.bmp'),
						pygame.image.load('sprites/canon35.bmp'),
						pygame.image.load('sprites/canon36.bmp'),
						pygame.image.load('sprites/canon37.bmp')]

		# Keep track of the canon current state
		self.active = False
		self.firing = False
		self.turn_canon_on = False

		# Will be used for changing images and animate the sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 100
		
		# Store the canon position as a decimal value.
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)

	def fire_canon(self):
		"""Activate the fire_laser animation."""
		self.sprite_list = self.fire_laser
		self.firing = True

	def load_canon(self):
		"""Activate the canon load animation and update method"""
		self.turn_canon_on = True
		self.sprite_list = self.loading_canon
		self.active = True
		# Will start the animation from the beggining if the player activate this before ending it completely
		self.image_value = 0

	def stop_canon(self):
		"""Activate the canon load animation backwards in a specific image"""
		self.turn_canon_on = False
		self.firing = False
		self.sprite_list = self.loading_canon
		self.image_value = 15

	def update(self):
		"""Moves gun sprite according to player movement"""
		# Update the decimal value of the gun
		self.x = self.player.rect.centerx
		self.y = self.player.rect.centery
		# Update the rect position
		self.rect.centerx =  self.x
		self.rect.centery = self.y

		if self.active:

			if pygame.time.get_ticks() - self.last_update > self.image_interval and self.turn_canon_on:
				self.image_value += 1
				self.last_update = pygame.time.get_ticks()

			elif pygame.time.get_ticks() - self.last_update > self.image_interval and not self.turn_canon_on:
				# Once the canon is set to turn off, we simply go through the load animation backwards
				self.image_value -= 1
				self.last_update = pygame.time.get_ticks()
				# Will stop the loop once the animation has ended
				if self.image_value == 0:
					self.active = False

			if self.image_value >= len(self.sprite_list):
				self.image_value = 0
				
			self.image = self.sprite_list[self.image_value]

		# if no animation is playing, simply use the default image
		if not self.active:
			self.image = self.main_image

	def draw(self):
		"""Draw the gun into the screen."""
		self.screen.blit(self.image, self.rect)
