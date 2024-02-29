import pygame
from pygame.sprite import Sprite
from pygame.locals import *

# This file have 1 parent class, and 3 child classes, each one representing a different enemy

class Enemy(Sprite):
	"""Parent class"""

	def __init__(self, game):
		super().__init__()
		"""Get the screen and settings"""
		self.screen = game.screen
		self.settings = game.settings

		# Will be used for changing images and animated sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 100

	def check_edges(self):
		"""Return True if this enemy is at the edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update_sprite(self):
		"""Here we just update the sprite"""

		if pygame.time.get_ticks() - self.last_update > self.image_interval:
			self.image_value += 1
			self.last_update = pygame.time.get_ticks()

		if self.image_value >= len(self.sprite_list):
			self.image_value = 0
		
		self.image = self.sprite_list[self.image_value]






class Enemy1(Enemy):
	"""Class to represent enemy 1, inherit from Enemy class"""

	def __init__(self, game):
		super().__init__(game)
		"""Initialize the enemy."""

		# Values that only enemy 1 is going to use
		self.hp = self.settings.e1_health
		self.points = self.settings.e1_value

		# Load the enemy image and get it's rect
		self.image = pygame.image.load('sprites/enemy-1.bmp')
		self.rect = self.image.get_rect()

		# Store the enemy exact horizontal position (we wont need the vertical position)
		self.x = float(self.rect.x)

		# List of all sprites for an animated sprite
		self.sprite_list = [pygame.image.load('sprites/enemy1_1.bmp'),
							pygame.image.load('sprites/enemy1_2.bmp'),
							pygame.image.load('sprites/enemy1_3.bmp'),
							pygame.image.load('sprites/enemy1_4.bmp'),
							pygame.image.load('sprites/enemy1_5.bmp'),
							pygame.image.load('sprites/enemy1_6.bmp'),
							pygame.image.load('sprites/enemy1_7.bmp'),
							pygame.image.load('sprites/enemy1_8.bmp'),
							pygame.image.load('sprites/enemy1_9.bmp'),
							pygame.image.load('sprites/enemy1_10.bmp')]


	def check_edges(self):
		"""Return True if this enemy is at the edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		"""Move the enemy to the right or left"""
		# Inherit update sprite function, the sprite list is used on it
		super().update_sprite()
		self.x += (self.settings.e1_speed * 
						self.settings.fleet_direction)
		self.rect.x = self.x


class Enemy2(Sprite):
	"""Class to represent enemy 2"""

	def __init__(self, game):
		super().__init__()
		"""Initialize the enemy."""
		
		# Values that only enemy 2 is going to use
		self.hp = self.settings.e2_health
		self.points = self.settings.e2_value

		# Load the enemy position and get it's rect
		self.image = pygame.image.load('sprites/enemy-1.bmp')
		self.rect = self.image.get_rect()

		self.sprite_list = [pygame.image.load('sprites/enemy1_1.bmp'),
							pygame.image.load('sprites/enemy1_2.bmp'),
							pygame.image.load('sprites/enemy1_3.bmp'),
							pygame.image.load('sprites/enemy1_4.bmp'),
							pygame.image.load('sprites/enemy1_5.bmp'),
							pygame.image.load('sprites/enemy1_6.bmp'),
							pygame.image.load('sprites/enemy1_7.bmp'),
							pygame.image.load('sprites/enemy1_8.bmp'),
							pygame.image.load('sprites/enemy1_9.bmp'),
							pygame.image.load('sprites/enemy1_10.bmp')]

		# Store the enemy exact horizontal position (we wont need the vertical position)
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Return True if this enemy is at the edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		"""Move the enemy to the right or left"""
		# Inherit update sprite function, the sprite list is used on it
		super().update_sprite()
		self.x += (self.settings.e2_speed * 
						self.settings.fleet_direction)
		self.rect.x = self.x



class Enemy3(Sprite):
	"""Class to represent enemy 3"""

	def __init__(self, game):
		super().__init__()
		"""Initialize the enemy."""
		
		# Values that only enemy 3 is going to use
		self.hp = self.settings.e3_health
		self.points = self.settings.e3_value

		# Load the enemy image and get it's rect
		self.image = pygame.image.load('sprites/enemy-1.bmp')
		self.rect = self.image.get_rect()

		self.sprite_list = [pygame.image.load('sprites/enemy1_1.bmp'),
							pygame.image.load('sprites/enemy1_2.bmp'),
							pygame.image.load('sprites/enemy1_3.bmp'),
							pygame.image.load('sprites/enemy1_4.bmp'),
							pygame.image.load('sprites/enemy1_5.bmp'),
							pygame.image.load('sprites/enemy1_6.bmp'),
							pygame.image.load('sprites/enemy1_7.bmp'),
							pygame.image.load('sprites/enemy1_8.bmp'),
							pygame.image.load('sprites/enemy1_9.bmp'),
							pygame.image.load('sprites/enemy1_10.bmp')]

		# Store the enemy exact horizontal position (we wont need the vertical position)
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Return True if this enemy is at the edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		"""Move the enemy to the right or left"""
		# Inherit update sprite function, the sprite list is used on it
		super().update_sprite()
		self.x += (self.settings.e3_speed * 
						self.settings.fleet_direction)
		self.rect.x = self.x