import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Gun(Sprite):
	"""A class to manage player's gun sprite so that animations can work separately"""

	def __init__(self, game):
		super().__init__()
		"""Create a gun object at the player current position."""
		self.screen = game.screen
		self.settings = game.settings
		self.game = game
		self.player = game.player

		# Load image, get rect and place inside of the player rect
		self.image = pygame.image.load('sprites/gun.bmp')
		self.rect = self.image.get_rect()
		self.rect.midtop = self.player.rect.midtop

		# List of all sprites for an animated sprite
		self.sprite_left = [pygame.image.load('sprites/gun_left1.bmp'),
							pygame.image.load('sprites/gun_left2.bmp'),
							pygame.image.load('sprites/gun_left3.bmp'),
							pygame.image.load('sprites/gun_left4.bmp'),
							pygame.image.load('sprites/gun_left5.bmp'),
							pygame.image.load('sprites/gun_left6.bmp')]

		self.sprite_right = [pygame.image.load('sprites/gun_right1.bmp'),
							pygame.image.load('sprites/gun_right2.bmp'),
							pygame.image.load('sprites/gun_right3.bmp'),
							pygame.image.load('sprites/gun_right4.bmp'),
							pygame.image.load('sprites/gun_right5.bmp'),
							pygame.image.load('sprites/gun_right6.bmp')]

		# Doesnt matter what list do you pass, it just can be empty
		self.sprite_list = self.sprite_left
		# This will control the update so that it doesnt go on forever
		self.firing = False
		# This will control so that it won't not keep repeting the same sprite over and over
		# Until the bullet has been deleted
		self.current_side = None
		self.old_side = None

		# Will be used for changing images and animate the sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 30
		
		# Store the gun position as a decimal value.
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)

	def fire_bullet(self, side):
		"""Will receive the side string, set the flag firing to true and decide the list of sprites accordingly"""
		if side == 'right':
			self.current_side = "right"
			self.sprite_list = self.sprite_right
			self.firing = True
		if side == 'left':
			self.current_side = 'left'
			self.sprite_list = self.sprite_left
			self.firing = True

	def update(self):
		"""Moves gun sprite according to player movement"""
		# Update the decimal value of the gun
		self.x = self.player.rect.midtop
		self.y = self.player.rect.midtop
		# Update the rect position
		self.rect.midtop =  self.x
		self.rect.midtop = self.y 

		# Will only shoot if the flag firing is true, and once the list ends, will only update the sprite if it's a different side
		# Otherwise it will replay the sprite until the bullet has been deleted due to how update functions are called in main.py
		if self.firing and self.current_side != self.old_side:
			if pygame.time.get_ticks() - self.last_update > self.image_interval:
				self.image_value += 1
				self.last_update = pygame.time.get_ticks()

			if self.image_value >= len(self.sprite_left):
				# Once the list has ended, we reset the flag, image_value 
				# and update the old_side so it doesn't replay the list on the same side
				self.image_value = 0
				self.firing = False
				self.old_side = self.current_side


			self.image = self.sprite_list[self.image_value]

	def draw(self):
		"""Draw the gun into the screen."""
		self.screen.blit(self.image, self.rect)
