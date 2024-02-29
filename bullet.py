import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Bullet(Sprite):
	"""A class to manage bullets fired from the player."""

	def __init__(self, game):
		super().__init__()
		"""Create a bullet object at the player current position."""
		self.screen = game.screen
		self.settings = game.settings
		self.player =  game.player

		# Load image, get rect and place on top of player
		self.image = pygame.image.load('sprites/bullet.bmp')
		self.rect = self.image.get_rect()

		# List of all sprites for an animated sprite
		self.sprite_list = [pygame.image.load('sprites/bullet1.bmp'),
							pygame.image.load('sprites/bullet2.bmp'),
							pygame.image.load('sprites/bullet3.bmp'),
							pygame.image.load('sprites/bullet4.bmp'),
							pygame.image.load('sprites/bullet5.bmp'),
							pygame.image.load('sprites/bullet6.bmp'),
							pygame.image.load('sprites/bullet7.bmp'),
							pygame.image.load('sprites/bullet8.bmp'),
							pygame.image.load('sprites/bullet9.bmp'),
							pygame.image.load('sprites/bullet10.bmp'),
							pygame.image.load('sprites/bullet11.bmp'),
							pygame.image.load('sprites/bullet12.bmp')]

		# Will be used for changing images and animate the sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 50
		
		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)


	def update(self):
		"""Moves the bullet up and animated the sprite."""
		# Update the decimal value of the bullet
		self.y -= self.settings.bullet_speed
		# Update the rect position
		self.rect.y =  self.y


		if pygame.time.get_ticks() - self.last_update > self.image_interval:
			self.image_value += 1
			self.last_update = pygame.time.get_ticks()

		if self.image_value >= len(self.sprite_list):
			self.image_value = 0
		
		self.image = self.sprite_list[self.image_value]


	def draw_bullet(self):
		"""Draw the bullet into the screen."""
		self.screen.blit(self.image, self.rect)


class LeftBullet(Bullet):
	def __init__(self, game):
		super().__init__(game)


		self.rect.bottomleft = self.player.rect.topleft

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)


	def update_left(self):
		super().update()

	def draw_bullet(self):
		"""Draw the bullet into the screen."""
		self.screen.blit(self.image, self.rect)

	def check_side(self):
		return "left"



class RightBullet(Bullet):
	def __init__(self, game):
		super().__init__(game)
		self.rect.bottomright = self.player.rect.topright

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)

	def update(self):
		super().update()

	def draw_bullet(self):
		"""Draw the bullet into the screen."""
		self.screen.blit(self.image, self.rect)

	def check_side(self):
		return "right"